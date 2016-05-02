import os
import tqdm
import heapq
import json

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict

import pprint

import mapper


graph = {}
def load_graph():
    global graph
    with open('graph.json','r') as datafile:
        graph = json.load(datafile,strict=False)

degree = {}
def load_degree():
    global degree
    with open('degree.json','r') as datafile:
        degree = json.load(datafile,strict=False)


def complement(recipenum):
  """ Complement of a recipe """
  f = open(PROCESS_DIR + str(recipenum) + '.txt', 'r')
  ingredients = set()
  for line in f:
    ingredients |= set([line.strip().lower()])
  f.close()

  d = defaultdict(float)
  top10 = heapq.nlargest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients
  for a in ingredients:
    i = correct(a)
    if i in graph and i not in top10:
      for k in graph[i]:
        if k in ingredients or k in top10:
          continue

        d[k] += min(1.0 * graph[i][k]/degree[i], 1.0 * graph[k][i]/degree[k])

  best = heapq.nlargest(10, d, key=lambda k: d[k])
  print
  for b in best:
    print b, d[b]
  print




