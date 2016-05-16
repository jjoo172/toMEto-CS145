""" Utilities used for all files
"""

import os
import tqdm
import heapq

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import pylab
import scipy.stats as stats

PROCESS_DIR = 'processed/'
MAPPER_OUT = 'mapper_out.txt'
MAPPER_TOP = 'mapper_top.txt'


#TODO:
def getrecipe_info(recipe_id):
  title = "title of the recipe"
  details = "the recipe itself"
  return [title, details]


def _correct(string):
  """ Fix non-ascii characters to '?' """
  l = list(string)
  for i in xrange(len(l)):
    if ord(l[i]) >= 128:
      l[i] = '?'
  return ''.join(l)


def _getmapping():
  """ Loads the ingredient mapping to reduce redundancy. Returns a dict """
  mapping = {}
  with open(MAPPER_OUT, 'r') as f:
    for line in f:
      a, b = line.rstrip('\n').split('\t')
      mapping[a] = b
  return mapping


def getrecipes(mapped=False, ignorenotmapped=False):
  """ Import database of recipes, located in PROCESS_DIR.

  Automatically uses _correct() to fix non-ascii characters.
  Set mapped=True to utilize mapping and reduce ingredient redundancy.
  Set ignorenotmapped=True to ignore ingredients that are not in mapped (why?).

  Returns a dict of recipe_id -> set of ingredients.
  """

  if mapped or ignorenotmapped:
    mapping = _getmapping()

  recipes = {}
  allfiles = [f for f in os.listdir(PROCESS_DIR) if os.path.isfile(PROCESS_DIR + f)]
  for filename in tqdm.tqdm(allfiles):
    with open(PROCESS_DIR + filename, 'r') as f:
      ingredients = set()
      for line in f:
        i = _correct(line.strip().lower())
        if ignorenotmapped and i not in mapping:
          continue
        if mapped and i in mapping:
          i = mapping[i]
        ingredients |= set([i])
      recipes[filename[:-4]] = ingredients
  return recipes

def substitute(original, recommendation):
    """ Substitute ingredient suggestions if they're too similar to
        an ingredient originally part of the recipe. One example
        of this occurance is suggesting 'white flour' when 'all-purpose flour'
        is already an ingredient """
    originalTokens = original.split(" ")
    recTokens = recommendation.split(" ")
    for item in originalTokens:
        if item in recTokens:
            return True
    return False

def gettop():
  """ Return a set of the top ingredients (in file specified by MAPPER_TOP) """
  topset = set([])
  with open(MAPPER_TOP, 'r') as f:
    for line in f:
      topset |= set([line.strip()])
  return topset



"""
TEST / DEBUG FUNCTIONS
"""

def showgraph(n, graph):
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


def histogram(degree, highest, binsize):
  x = [k for k in degree]
  y = [degree[k] for k in degree]
  plt.hist((x, y), bins=np.arange(0, highest, binsize))
  plt.show()


def loglogplot(degree):
  vals = degree.values()
  vals = filter(lambda x: x > 0, vals)
  vals.sort()
  ranks = [i for i in range(len(vals))]
  ranks.reverse()
  plt.loglog(ranks, vals, basex=10, basey=10)
  plt.show()

def qqplot(degree):
  vals = degree.values()
  stats.probplot(np.array(vals), dist="lognorm(1.5)", plot = pylab)
  pylab.show()








def dump_json(d, filename):
    with open(filename, 'w') as outfile:
        json.dump(d, outfile)
