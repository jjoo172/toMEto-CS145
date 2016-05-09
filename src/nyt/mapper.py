""" USAGE:

# Generate mapper_out.txt, mapper_top.txt
>> python mapper.py

Notes:
- graph[x] is the set of recipes that "use" ingredient x
- degree[x] = len(graph[x])
- degree and mapping are disjoint, aka ingredient x is in exactly one
- mapping is currently 1:1
- mapping[x] is guaranteed to NOT be in mapping

"""

import tqdm
import random

import analyzerutils


MIN_DEGREE = 10
DEBUG = False


def writeToFile():
  with open(analyzerutils.MAPPER_OUT, 'w') as f:
    for d in mapping:
      f.write('%s\t%s\n' % (d, mapping[d]))

  with open(analyzerutils.MAPPER_TOP, 'w') as f:
    for d in degree:
      if degree[d] >= MIN_DEGREE:
        f.write('%s\n' % d)

def importall():
  global graph, degree, recipes, mapping

  graph = {}
  degree = {}
  recipes = analyzerutils.getrecipes()
  mapping = {}

  for recipe_id in tqdm.tqdm(recipes):
    ingredients = recipes[recipe_id]
    for a in ingredients:
      if a not in graph:
        graph[a] = set([])

      graph[a] |= set([recipe_id])

  for g in graph:
    degree[g] = len(graph[g])

  if DEBUG:  
    print 'len(degree) =', len(degree)

  t1()    # ,
  t6()    # (

  t5()    # ' or '
  t3()    # replace with top

  t4()    # s
  t7()    # first word

  t5()    # ' or '
  t3()    # replace with top

  if DEBUG:  
    print 'len(degree) =', len(degree)
    print 'len(mapping) = ', len(mapping)

def remove(rm):
  for d in rm:
    d2 = mapping[d]
    graph[d2] |= graph[d]
    degree[d2] = len(graph[d2])
    for m2 in mapping:
      if mapping[m2] == d:
        mapping[m2] = mapping[d]

    del graph[d]
    del degree[d]

def t1():
  rm = set([])
  for d in degree:
    if degree[d] < MIN_DEGREE:
      k = d.find(',')
      if k >= 0:
        d2 = d[:k]
        if d2 in degree:
          mapping[d] = d2
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't1, %d' % len(rm)

def t3():
  top = set([])
  rm = set([])

  for d in degree:
    if degree[d] >= MIN_DEGREE:
      top |= set([d])

  for d in degree:
    if d not in top:
      matches = []
      for d2 in top:
        if (' ' + d2 + ' ') in d or \
            (' ' + d2 + ',') in d or d.find(d2 + ' ') == 0 or \
            d.find(d2 + ',') == 0 or \
            (d.find(' ' + d2) > 0 and d.find(' ' + d2) == len(d) - len(d2) - 1):
          matches.append(d2)

      if len(matches) == 1:
        mapping[d] = matches[0]
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
            rm |= set([d])
            break

  remove(rm)
  if DEBUG:  
    print 't3, %d' % len(rm)

def t4():
  rm = set([])
  for d in degree:
    d2 = d[:-1]
    if d[-1] == 's':
      d2 = d[:-1]
      if d2 in degree:
        if degree[d2] > d:
          mapping[d] = d2
          rm |= set([d])
        else:
          mapping[d2] = d
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
  for d in degree:
    k = d.find(' or ')
    if k >= 0:
      d2 = d[:k]
      d3 = d[k + 4:]
      if d2 in degree and d3 not in degree:
        mapping[d] = d2
        rm |= set([d])
      if d3 in degree and d2 not in degree:
        mapping[d] = d3
        rm |= set([d])
      if d2 in degree and d3 in degree:
        i += 1

  remove(rm)
  if DEBUG:  
    print 't5, %d' % len(rm)
    print i

def t6():
  rm = set([])
  for d in degree:
    if degree[d] < MIN_DEGREE:
      k = d.find('(')
      if k >= 1:
        d2 = d[:k - 1]
        if d2 in degree:
          mapping[d] = d2
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't6, %d' % len(rm)

def t7():
  rm = set([])
  for d in degree:
    if degree[d] < MIN_DEGREE:
      k = d.find(' ')
      if k >= 0:
        d2 = d[k+1:]
        if d2 in degree:
          mapping[d] = d2
          rm |= set([d])
        else:
          d2 += 's'
          if d2 in degree:
            mapping[d] = d2
            rm |= set([d])

  remove(rm)
  if DEBUG:  
    print 't7, %d' % len(rm)


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

def test2(s):
  for d in degree:
    if s in d:
      print d, degree[d]

def test3():
  top = set([])
  rm = set([])

  for d in degree:
    if degree[d] >= MIN_DEGREE:
      top |= set([d])

  print len(top)

def test4():
  i=0
  for d in mapping:
    if random.randint(1, 10) == 1:
      print '%s --> %s' % (d, mapping[d])
      i+=1
      if i > 100:
        break


# Write map and top ingredients to file
if __name__ == '__main__':
  importall()
  writeToFile()
