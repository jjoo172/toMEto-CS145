""" USAGE:

Enter the python environment by running 'python'

>>> execfile('analyzer.py')
>>> graph = {}
>>> degree = {}
>>> importall()

>>> complement(420)
>>> showgraph(1000)

"""


import os
import tqdm
import heapq

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


PROCESS_DIR = 'processed/'

def correct(string):
  """ Fix non-ascii characters to '?' """
  l = list(string)
  for i in xrange(len(l)):
    if ord(l[i]) >= 128:
      l[i] = '?'
  return ''.join(l)

def load_map():
    """ Loads the ingredient mapping to reduce redundancy """
    global map
    map = {}
    with open('out.txt','r') as f:
        for line in f:
            a,b = line.rstrip('\n').split('\t')
            map[a] = b

def PMI(a, b):
    return np.log(float(graph[a][b]) / tot_recipe) /\
            (num_recipe[a] / tot_recipe * num_recipe[b] / tot_recipe)



def importfile(filename):
  """ First time importing ... """
  f = open(PROCESS_DIR + filename, 'r')
  ingredients = set()
  for line in f:
    ingredients |= set([line.strip().lower()])
  f.close()

  for a in ingredients:
    if a not in map:
        continue
    x = map[correct(a)]
    num_recipe[x] = num_recipe.get(x, 0.0) + 1.0
    for b in ingredients:
      if b not in map:
        continue
      y = map[correct(b)]
      if x != y:
        if x not in graph:
          graph[x] = {}
        if y not in graph[x]:
          graph[x][y] = 0

        graph[x][y] += 1

def importfile2(filename, top1000):
  """ Second time importing, only take top1000 ... """
  f = open(PROCESS_DIR + filename, 'r')
  ingredients = set()
  for line in f:
    ingredients |= set([line.strip().lower()])
  f.close()

  for a in ingredients:
    if a not in map:
        continue
    x = map[correct(a)]
    num_recipe[x] = num_recipe.get(x, 0.0) + 1.0
    for b in ingredients:
      if b not in map:
        continue
      y = map[correct(b)]
      if x != y and x in top1000 and y in top1000:
        if x not in graph:
          graph[x] = {}
        if y not in graph[x]:
          graph[x][y] = 0
        graph[x][y] += 1


def importall():
  """ Call to import everything """
  global graph, degree, num_recipe, tot_recipe

  # graph = {}
  # degree = {}
  # allfiles = [f for f in os.listdir(PROCESS_DIR) if os.path.isfile(PROCESS_DIR + f)]
  # tot_recipe = len(allfiles)
  #
  # for f in tqdm.tqdm(allfiles):
  #   importfile(f)
  #
  # for g in graph:
  #   degree[g] = 0.0
  #   for z in graph[g]:
  #     degree[g] += graph[g][z]
  #
  # top1000 = set(heapq.nlargest(1000, degree, key=lambda k: degree[k]))
  graph = {}
  degree = {}
  num_recipe = {}
  allfiles = [f for f in os.listdir(PROCESS_DIR) if os.path.isfile(PROCESS_DIR + f)]
  tot_recipe = len(allfiles)
  for f in tqdm.tqdm(allfiles):
      importfile(f)

  for g in graph:
    degree[g] = 0.0
    for z in graph[g]:
      degree[g] += PMI(g,z)


def complement(recipenum):
  """ Complement of a recipe """
  f = open(PROCESS_DIR + str(recipenum) + '.txt', 'r')
  ingredients = set()
  for line in f:
    ingredients |= set([line.strip().lower()])
  f.close()

  d = {}
  top10 = heapq.nsmallest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients
  for a in ingredients:
    i = correct(a)
    if i in graph and i not in top10:
      for k in graph[i]:
        if k in ingredients or k in top10:
          continue
        if k not in d:
          d[k] = 0

        d[k] += PMI(i, k)/degree[i]
        # d[k] += min(1.0 * graph[i][k]/degree[i], 1.0 * graph[k][i]/degree[k])

  best = heapq.nsmallest(10, d, key=lambda k: d[k])
  print
  for b in best:
    print b, d[b]
  print

def showgraph(n):
  """ Show top n nodes by degree """
  G = nx.Graph()
  alle = {}
  for i in tqdm.tqdm(graph):
    if degree[i] > 50:
      top10 = heapq.nlargest(10, graph[i], key=lambda k: graph[i][k])
      for z in xrange(min(10, len(top10))):
        alle[(i, top10[z])] = graph[i][top10[z]]

  top10 = heapq.nlargest(n, alle, key=lambda k: alle[k])
  for t in top10:
    for i in t[0]:
      if ord(i) > 128:
        print t[0]
    for i in t[1]:
      if ord(i) > 128:
        print t[1]


  G.add_edges_from(top10)

  nx.draw(G, with_labels=True)
  plt.show()




"""
TEST / DEBUG FUNCTIONS
"""


def prune():
  num = 0
  for a in graph:
    for b in graph:
      if a == b:
        continue
      if a in b:
        print '%s <IN> %s' % (a, b)
        num += 1
        break
    if num > 100:
      break

def least():
  for k in degree:
    if degree[k] == 1:
      print k

def histogram(highest, binsize):
  x = [k for k in degree]
  y = [degree[k] for k in degree]
  plt.hist((x, y), bins=np.arange(0, highest, binsize))
  plt.show()

def dump_graph():
    with open('graph.json', 'w') as outfile:
        json.dump(graph, outfile)

def dump_degree():
    with open('degree.json', 'w') as outfile:
        json.dump(degree, outfile)



