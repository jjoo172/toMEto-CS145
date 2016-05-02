""" USAGE:

import mapper
m = mapper.mapper()
m.importall()
m.mapping['egg']     # 'eggs'


Notes:
- m.graph[x] is the set of recipes that "use" ingredient x
- m.degree[x] = len(m.graph[x])
- m.degree and m.mapping are disjoint, aka ingredient x is in exactly one
- m.mapping is currently 1:1
- m.mapping[x] is guaranteed to NOT be in m.mapping

"""


import os
import tqdm
import random


class mapper():
  PROCESS_DIR = 'processed/'
  MIN_DEGREE = 10

  DEBUG = False

  def correct(self, string):
    """ Fix non-ascii characters to '?' """
    l = list(string)
    for i in xrange(len(l)):
      if ord(l[i]) >= 128:
        l[i] = '?'
    return ''.join(l)

  def importfile(self, filename):
    f = open(self.PROCESS_DIR + filename, 'r')
    ingredients = set()
    for line in f:
      ingredients |= set([line.strip().lower()])
    f.close()

    for a in ingredients:
      x = self.correct(a)
      if x not in self.graph:
        self.graph[x] = set([])

      self.graph[x] |= set([filename])


  def importall(self):
    self.graph = {}
    self.degree = {}
    allfiles = [f for f in os.listdir(self.PROCESS_DIR) if os.path.isfile(self.PROCESS_DIR + f)]
    for f in tqdm.tqdm(allfiles):
      self.importfile(f)

    for g in self.graph:
      self.degree[g] = len(self.graph[g])

    self.mapping = {}

    if self.DEBUG:  
      print 'len(degree) =', len(self.degree)

    self.t1()    # ,
    self.t6()    # (

    self.t5()    # ' or '
    self.t3()    # replace with top

    self.t4()    # s
    self.t7()    # first word

    self.t5()    # ' or '
    self.t3()    # replace with top

    if self.DEBUG:  
      print 'len(degree) =', len(self.degree)
      print 'len(mapping) = ', len(self.mapping)


  def remove(self, rm):
    for d in rm:
      d2 = self.mapping[d]
      self.graph[d2] |= self.graph[d]
      self.degree[d2] = len(self.graph[d2])
      for m2 in self.mapping:
        if self.mapping[m2] == d:
          self.mapping[m2] = self.mapping[d]

      del self.graph[d]
      del self.degree[d]


  def t1(self):
    rm = set([])
    for d in self.degree:
      if self.degree[d] < self.MIN_DEGREE:
        k = d.find(',')
        if k >= 0:
          d2 = d[:k]
          if d2 in self.degree:
            self.mapping[d] = d2
            rm |= set([d])
          else:
            d2 += 's'
            if d2 in self.degree:
              self.mapping[d] = d2
              rm |= set([d])

    self.remove(rm)
    if self.DEBUG:  
      print 't1, %d' % len(rm)


  def t3(self):
    top = set([])
    rm = set([])

    for d in self.degree:
      if self.degree[d] >= self.MIN_DEGREE:
        top |= set([d])

    for d in self.degree:
      if d not in top:
        matches = []
        for d2 in top:
          if (' ' + d2 + ' ') in d or \
              (' ' + d2 + ',') in d or d.find(d2 + ' ') == 0 or \
              d.find(d2 + ',') == 0 or \
              (d.find(' ' + d2) > 0 and d.find(' ' + d2) == len(d) - len(d2) - 1):
            matches.append(d2)

        if len(matches) == 1:
          self.mapping[d] = matches[0]
          rm |= set([d])

        else:
          for m1 in matches:
            ok = True
            for m2 in matches:
              if m2 not in m1:
                ok = False
                break
            if ok:
              self.mapping[d] = m1
              rm |= set([d])
              break

    self.remove(rm)
    if self.DEBUG:  
      print 't3, %d' % len(rm)


  def t4(self):
    rm = set([])
    for d in self.degree:
      d2 = d[:-1]
      if d[-1] == 's':
        d2 = d[:-1]
        if d2 in self.degree:
          if self.degree[d2] > d:
            self.mapping[d] = d2
            rm |= set([d])
          else:
            self.mapping[d2] = d
            rm |= set([d2])

    for d in rm:
      for d2 in rm:
        if d[-1] == 's':
          assert(d[:-1] != d2)

    self.remove(rm)
    if self.DEBUG:  
      print 't4, %d' % len(rm)


  def t5(self):
    i = 0
    rm = set([])
    for d in self.degree:
      k = d.find(' or ')
      if k >= 0:
        d2 = d[:k]
        d3 = d[k + 4:]
        if d2 in self.degree and d3 not in self.degree:
          self.mapping[d] = d2
          rm |= set([d])
        if d3 in self.degree and d2 not in self.degree:
          self.mapping[d] = d3
          rm |= set([d])
        if d2 in self.degree and d3 in self.degree:
          i += 1

    self.remove(rm)
    if self.DEBUG:  
      print 't5, %d' % len(rm)
      print i


  def t6(self):
    rm = set([])
    for d in self.degree:
      if self.degree[d] < self.MIN_DEGREE:
        k = d.find('(')
        if k >= 1:
          d2 = d[:k - 1]
          if d2 in self.degree:
            self.mapping[d] = d2
            rm |= set([d])
          else:
            d2 += 's'
            if d2 in self.degree:
              self.mapping[d] = d2
              rm |= set([d])

    self.remove(rm)
    if self.DEBUG:  
      print 't6, %d' % len(rm)


  def t7(self):
    rm = set([])
    for d in self.degree:
      if self.degree[d] < self.MIN_DEGREE:
        k = d.find(' ')
        if k >= 0:
          d2 = d[k+1:]
          if d2 in self.degree:
            self.mapping[d] = d2
            rm |= set([d])
          else:
            d2 += 's'
            if d2 in self.degree:
              self.mapping[d] = d2
              rm |= set([d])

    self.remove(rm)
    if self.DEBUG:  
      print 't7, %d' % len(rm)




  """""""""""""""""""""""""""""""""""""""
  FOR TEST/DEBUG
  """""""""""""""""""""""""""""""""""""""

  def test(self):
    i=0
    for d in self.degree:
      if random.randint(1, 10) == 1 and self.degree[d] < self.MIN_DEGREE:
        print d, self.degree[d]
        i+=1
        if i > 100:
          break

  def test2(self, s):
    for d in self.degree:
      if s in d:
        print d, self.degree[d]

  def test3(self):
    top = set([])
    rm = set([])

    for d in self.degree:
      if self.degree[d] >= self.MIN_DEGREE:
        top |= set([d])

    print len(top)

  def test4(self):
    i=0
    for d in self.mapping:
      if random.randint(1, 10) == 1:
        print '%s --> %s' % (d, self.mapping[d])
        i+=1
        if i > 100:
          break

  def test5(self):
    outfile = 'out.txt'
    with open(outfile, 'w') as f:
      for d in self.mapping:
        f.write('%s\t%s\n' % (d, self.mapping[d]))
