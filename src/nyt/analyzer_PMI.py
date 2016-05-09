""" USAGE: 
  >> python analyzer_PMI.py
"""

import os
import tqdm
import heapq
from collections import defaultdict
import numpy as np

import utils


def PMI(a, b):
    return np.log(float(graph[a][b]) / len(recipes)) /\
            (num_recipe[a] / len(recipes) * num_recipe[b] / len(recipes))


def importall():
  """ Call to import everything """
  global graph, degree, recipes, recipes2, top, num_recipe

  graph = defaultdict(lambda: defaultdict(float))
  degree = defaultdict(float)
  recipes = utils.getrecipes(mapped=True, ignorenotmapped=True)
  recipes2 = utils.getrecipes(mapped=False, ignorenotmapped=False)
  top = utils.gettop()
  num_recipe = defaultdict(float)

  for recipe_id in tqdm.tqdm(recipes):
    ingredients = recipes[recipe_id]

    for a in ingredients:
      num_recipe[a] += 1.0;
      for b in ingredients:
        if a != b and a in top and b in top:
          graph[a][b] += 1.0

  for a in graph:
    for b in graph[a]:
      degree[a] += PMI(a, b)


def complement(recipe_id):
  """ Complement of a recipe """
  ingredients = recipes2[recipe_id]

  d = defaultdict(float)
  top10 = heapq.nsmallest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients
  for a in ingredients:
    if a in graph and a not in top10:
      for b in graph[a]:
        if b in ingredients or b in top10:
          continue
        d[b] += PMI(a, b) / degree[a]

  return heapq.nsmallest(10, d, key=lambda k: d[k])


def writeToFile(filename):
  with open(filename, 'w') as out:
    for recipe_id in tqdm.tqdm(recipes):
      best = complement(recipe_id)
      out.write('%s\t%s\n' % (recipe_id, '\t'.join(best)))


if __name__ == '__main__':
  importall()
  writeToFile(__file__[:-3] + '.txt')
