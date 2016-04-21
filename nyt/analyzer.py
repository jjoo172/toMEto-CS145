import os
import tqdm
import heapq

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


PROCESS_DIR = 'processed/'

def correct(string):
  l = list(string)
  for i in xrange(len(l)):
    if ord(l[i]) >= 128:
      l[i] = '?'
  return ''.join(l)

def importfile(filename):
  f = open(PROCESS_DIR + filename, 'r')
  ingredients = set()
  for line in f:
    ingredients |= set([line.strip().lower()])
  f.close()

  for a in ingredients:
    for b in ingredients:
      x = correct(a)
      y = correct(b)
      if x != y:
        if x not in graph:
          graph[x] = {}
        if y not in graph[x]:
          graph[x][y] = 0

        graph[x][y] += 1


def importall():
  allfiles = [f for f in os.listdir(PROCESS_DIR) if os.path.isfile(PROCESS_DIR + f)]
  for f in tqdm.tqdm(allfiles):
    importfile(f)

  for g in graph:
    degree[g] = 0.0
    for z in graph[g]:
      degree[g] += graph[g][z]
    for z in graph[g]:
      graph[g][z] /= degree[g]


def complement(recipenum):
  f = open(PROCESS_DIR + str(recipenum) + '.txt', 'r')
  ingredients = set()
  for line in f:
    ingredients |= set([line.strip().lower()])
  f.close()

  d = {}
  for a in ingredients:
    i = correct(a)
    for k in graph[i]:
      if k in ingredients:
        continue

      if k not in d:
        d[k] = 0

      d[k] += min(graph[i][k], graph[k][i])

  best = heapq.nlargest(10, d, key=lambda k: d[k])
  print
  for b in best:
    print b, d[b]
  print


def showgraph(n):
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

