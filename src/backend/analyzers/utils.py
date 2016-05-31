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

import codecs
import HTMLParser

parser = HTMLParser.HTMLParser()

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

DEFAULT_PROCESSED_DIR = FILE_DIR + '/../data/processed/'
DEFAULT_MAPPING_FILE = FILE_DIR + '/../data/nyt_mapper_mapping.txt'
DEFAULT_TOP_FILE = FILE_DIR + '/../data/nyt_mapper_top.txt'



"""
RECIPE LOADING
"""

def getrecipes(directory=DEFAULT_PROCESSED_DIR, mapped=False, mapping_file=None):
  """ Import database of recipes, located in PROCESS_DIR.

  Set mapped=True to utilize mapping and reduce ingredient redundancy.

  Returns a dict of recipe_id -> set of ingredients.
  """

  if mapped:
    if not mapping_file:
      mapping_file = DEFAULT_MAPPING_FILE
    mapping = getmapping(mapping_file)

  recipes = {}
  allfiles = [f for f in os.listdir(directory) if os.path.isfile(directory + f)]
  for filename in tqdm.tqdm(allfiles):
    with codecs.open(directory + filename, 'r', 'utf-8') as f:
      # First line is title, second line is ingredients (tab separated)
      f.readline()
      line2 = f.readline()

      # Tokenize line2, extract ingredients, and put into set
      ingredients = set()
      split2 = line2.split('\t')
      for i in split2:
        i = i.strip().lower()
        if i:       # Need this check to handle no-ingredient case
          if mapped and i in mapping:
            i = mapping[i]
          ingredients |= set([i])

      # Insert set into dictionary
      recipes[filename[:-4]] = ingredients

  return recipes


def getrecipe_info(recipe_id, directory=DEFAULT_PROCESSED_DIR):
  """ Get the recipe title and body.

  Returns a tuple of (title, body)
  """
  with open(directory + recipe_id + '.txt', 'r') as f:
    content = f.read()

    # Get title (line 1)
    i = content.find('\n')
    title = content[:i]
    title = str(parser.unescape(title))
    if title.rsplit(None, 1)[-1] == 'Recipe':
       title = title.rsplit(' ', 1)[0]

    # Get body (lines 3 to end)
    i = content.find('\n', i+1)
    body = content[i+1:]

    return title, body



"""
MAPPING LOADING
"""

def getmapping(mapping_file=DEFAULT_MAPPING_FILE):
  """ Loads the ingredient mapping to reduce redundancy. Returns a dict """
  mapping = {}
  with codecs.open(mapping_file, 'r', 'utf-8') as f:
    for line in f:
      a, b = line.rstrip('\n').split('\t')
      mapping[a] = b
  return mapping

def gettop(top_file=DEFAULT_TOP_FILE):
  """ Return a set of the top ingredients (in file specified by MAPPER_TOP) """
  topset = set([])
  with codecs.open(top_file, 'r', 'utf-8') as f:
    for line in f:
      topset |= set([line.strip()])
  return topset



"""
MISCELLANEOUS
"""

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

def _correct(string):
  """ DEPRECATED. NO LONGER NEEDED WITH UNICODE ENCODING.

  Fix non-ascii characters to '?'
  """
  assert(False)

  l = list(string)
  for i in xrange(len(l)):
    if ord(l[i]) >= 128:
      l[i] = '?'
  return ''.join(l)


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
