""" Maps allrecipes ingredients to NYT ingredients, used by allrecipes_parser.py
"""
import tqdm
import random

from collections import defaultdict


MIN_DEGREE = 10
DEBUG = True


def _clean(a):
  """ Clean prefixes from an ingredient (such as numbers and quantifiers) """
  split = a.split(' ')
  while len(split) > 0:
    if '1' in split[0] or \
       '2' in split[0] or \
       '3' in split[0] or \
       '4' in split[0] or \
       '5' in split[0] or \
       '6' in split[0] or \
       '7' in split[0] or \
       '8' in split[0] or \
       '9' in split[0] or \
       '0' in split[0]:
      split = split[1:]
    else:
      break

  quantities = ['cup', 'dash', 'drop', 'gallon', 'liter', 'ounce', 'pound', 'pinch', 
    'pint', 'quart', 'shot', 'spoon', 'can', 'jar', 'tub', 'box', 'fluid', 'package']

  while len(split) > 1:
    found = False
    for q in quantities:
      if q in split[0]:
        split = split[1:]
        found = True
        break
    if not found:
      break

  if len(split) > 0 and split[0] == 'of':
    split = split[1:]

  b = ' '.join(split)
  while len(b) > 0 and b[-1] == ':':
    b = b[:-1]

  if len(b) > 0:
    mapping[a] = b
    invmapping[b] |= set([a])
    return b

  return None

def main(recipes_, nytmapping_, nyttop_):
  global graph, degree, recipes, mapping, invmapping, nytmapping, nyttop

  graph = defaultdict(set)
  degree = {}
  recipes = recipes_
  mapping = {}
  invmapping = defaultdict(set)
  
  nytmapping = nytmapping_
  nyttop = nyttop_

  for recipe_id in tqdm.tqdm(recipes):
    ingredients = recipes[recipe_id]
    for a in ingredients:
      a = _clean(a)
      if not a:
        continue

      if a not in graph:
        graph[a] = set([])

      graph[a] |= set([recipe_id])

  for g in graph:
    degree[g] = len(graph[g])

  if DEBUG:  
    print 'len(degree) =', len(degree)

  t1()    # ,
  t2()    # :
  t6()    # (

  t5()    # ' or '
  t3()    # replace with nyttop
  t8()    # check direct mapping...
  t9()    # check replacement mapping...

  t4()    # s
  t7()    # first word
  t5()    # ' or '

  if DEBUG:  
    print 'len(degree) =', len(degree)
    print 'len(mapping) = ', len(mapping)

  return mapping

def remove(rm):
  for d in tqdm.tqdm(rm):
    d2 = mapping[d]
    graph[d2] |= graph[d]
    degree[d2] = len(graph[d2])
    for m2 in invmapping[d]:
      mapping[m2] = mapping[d]
    invmapping[mapping[d]] |= invmapping[d]

    del graph[d]
    del degree[d]
    del invmapping[d]

def t1():
  rm = set([])
  for d in tqdm.tqdm(degree):
    if degree[d] < MIN_DEGREE:
      k = d.find(',')
      if k >= 0:
        d2 = d[:k]
        if d2 in degree:
          mapping[d] = d2
          invmapping[d2] |= set([d])
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            invmapping[d2] |= set([d])
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't1, %d' % len(rm)

def t2():
  rm = set([])
  for d in tqdm.tqdm(degree):
    if degree[d] < MIN_DEGREE:
      k = d.find(':')
      if k >= 0:
        d2 = d[:k]
        if d2 in degree:
          mapping[d] = d2
          invmapping[d2] |= set([d])
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            invmapping[d2] |= set([d])
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't2, %d' % len(rm)

def t3():
  rm = set([])
  for d in tqdm.tqdm(degree):
    if d not in nyttop:
      matches = []
      for d2 in nyttop:
        if (' ' + d2 + ' ') in d or \
            (' ' + d2 + ',') in d or d.find(d2 + ' ') == 0 or \
            d.find(d2 + ',') == 0 or \
            (d.find(' ' + d2) > 0 and d.find(' ' + d2) == len(d) - len(d2) - 1):
          matches.append(d2)

      if len(matches) == 1:
        mapping[d] = matches[0]
        invmapping[matches[0]] |= set([d])
        rm |= set([d])

      else:
        for m1 in matches:
          ok = True
          for m2 in matches:
            if m2 not in m1:
              ok = False
              break
          if ok:
            mapping[d] = m1
            invmapping[m1] |= set([d])
            rm |= set([d])
            break

  remove(rm)
  if DEBUG:  
    print 't3, %d' % len(rm)

def t4():
  rm = set([])
  for d in tqdm.tqdm(degree):
    d2 = d[:-1]
    if d[-1] == 's':
      d2 = d[:-1]
      if d2 in degree:
        if degree[d2] > d:
          mapping[d] = d2
          invmapping[d2] |= set([d])
          rm |= set([d])
        else:
          mapping[d2] = d
          invmapping[d] |= set([d2])
          rm |= set([d2])

  for d in rm:
    for d2 in rm:
      if d[-1] == 's':
        assert(d[:-1] != d2)

  remove(rm)
  if DEBUG:  
    print 't4, %d' % len(rm)

def t5():
  i = 0
  rm = set([])
  for d in tqdm.tqdm(degree):
    k = d.find(' or ')
    if k >= 0:
      d2 = d[:k]
      d3 = d[k + 4:]
      if d2 in degree and d3 not in degree:
        mapping[d] = d2
        invmapping[d2] |= set([d])
        rm |= set([d])
      if d3 in degree and d2 not in degree:
        mapping[d] = d3
        invmapping[d3] |= set([d])
        rm |= set([d])
      if d2 in degree and d3 in degree:
        i += 1

  remove(rm)
  if DEBUG:  
    print 't5, %d' % len(rm)
    print i

def t6():
  rm = set([])
  for d in tqdm.tqdm(degree):
    if degree[d] < MIN_DEGREE:
      k = d.find('(')
      if k >= 1:
        d2 = d[:k - 1]
        if d2 in degree:
          mapping[d] = d2
          invmapping[d2] |= set([d])
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            invmapping[d2] |= set([d])
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't6, %d' % len(rm)

def t7():
  rm = set([])
  for d in tqdm.tqdm(degree):
    if degree[d] < MIN_DEGREE:
      k = d.find(' ')
      if k >= 0:
        d2 = d[k+1:]
        if d2 in degree:
          mapping[d] = d2
          invmapping[d2] |= set([d])
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            invmapping[d2] |= set([d])
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't7, %d' % len(rm)

def t8():
  rm = set([])
  for d in tqdm.tqdm(degree):
    matches = []
    for d2 in nytmapping:
      if (' ' + d2 + ' ') in d or \
          (' ' + d2 + ',') in d or d.find(d2 + ' ') == 0 or \
          d.find(d2 + ',') == 0 or \
          (d.find(' ' + d2) > 0 and d.find(' ' + d2) == len(d) - len(d2) - 1):
        matches.append(d2)

    if len(matches) >= 1:
      ok = True
      last = None
      for m1 in matches:
        if not last:
          last = nytmapping[m1]
        else:
          if nytmapping[m1] != last:
           ok = False
           break
      if ok and last:
        mapping[d] = last
        invmapping[nytmapping[m1]] |= set([d])
        rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't8, %d' % len(rm)

def t9():
  rm = set([])
  for d in tqdm.tqdm(degree):
    matches = []
    for d2 in nytmapping:
      if (' ' + d2 + ' ') in d or \
          (' ' + d2 + ',') in d or d.find(d2 + ' ') == 0 or \
          d.find(d2 + ',') == 0 or \
          (d.find(' ' + d2) > 0 and d.find(' ' + d2) == len(d) - len(d2) - 1):
        matches.append(d2)

    if len(matches) >= 1:
      for m1 in matches:
        ok = True
        m1 = nytmapping[m1]
        for m2 in matches:
          m2 = nytmapping[m2]
          if m2 not in m1:
            ok = False
            break
        if ok:
          mapping[d] = m1
          invmapping[m1] |= set([d])
          rm |= set([d])
          break

  remove(rm)
  if DEBUG:  
    print 't9, %d' % len(rm)

def t10():
  rm = set([])
  for d in tqdm.tqdm(degree):
    matches = []
    for d2 in nytmapping:
      if (' ' + d2 + ' ') in d or \
          (' ' + d2 + ',') in d or d.find(d2 + ' ') == 0 or \
          d.find(d2 + ',') == 0 or \
          (d.find(' ' + d2) > 0 and d.find(' ' + d2) == len(d) - len(d2) - 1):
        matches.append(d2)

    if len(matches) >= 1:
      for m1 in matches:
        ok = True
        for m2 in matches:
          if m2 not in m1:
            ok = False
            break
        if ok:
          mapping[d] = nytmapping[m1]
          invmapping[nytmapping[m1]] |= set([d])
          rm |= set([d])
          break

  remove(rm)
  if DEBUG:  
    print 't10, %d' % len(rm)

"""""""""""""""""""""""""""""""""""""""
FOR TEST/DEBUG
"""""""""""""""""""""""""""""""""""""""

def test():
  i=0
  for d in degree:
    if random.randint(1, 10) == 1 and degree[d] < MIN_DEGREE:
      print d, degree[d]
      i+=1
      if i > 100:
        break

def test4():
  i=0
  for d in mapping:
    if random.randint(1, 10) == 1:
      print '%s --> %s' % (d, mapping[d])
      i+=1
      if i > 100:
        break

def test5():
  sum1, sum2 = 0, 0
  for d in degree:
    if d in nyttop:
      sum1 += degree[d]
    else:
      sum2 += degree[d]
  print sum1
  print sum2

def test6():
  for k in degree:
    if degree[k] >= MIN_DEGREE and k not in nyttop:
      print k, degree[k]
