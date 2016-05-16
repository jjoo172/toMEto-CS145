""" USAGE: 
  >> python analyzer_PMI2.py
"""

import os
import tqdm
import heapq
from collections import defaultdict
import numpy as np

import utils
utils.PROCESS_DIR = 'processed2/' # combined dataset


def PMI(a, b):
    num = float(graph[a][b]) / len(recipes)
    tmp1 = float(num_recipe[a]) / len(recipes)
    tmp2 = float(num_recipe[b]) / len(recipes)
    return np.log(num / (tmp1 * tmp2))


def importall():
  """ Call to import everything """
  global graph, degree, recipes, top, num_recipe

  graph = defaultdict(lambda: defaultdict(float))
  degree = defaultdict(float)
  recipes = utils.getrecipes(mapped=True)
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
      degree[a] += graph[a][b]


def complement(recipe_id):
  """ Complement of a recipe """
  ingredients = recipes[recipe_id]
  global d

  d = defaultdict(float)
  top10 = heapq.nlargest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients
  for a in ingredients:
    if a in graph and a not in top10:
      for b in graph[a]:
        if b in ingredients or b in top10:
          continue
        if b in d:
          d[b] = min(d[b], PMI(a, b))
        else:
          d[b] = PMI(a,b)

  return heapq.nlargest(10, d, key=lambda k: d[k])


def writeToFile(filename):
  with open(filename, 'w') as out:
    for recipe_id in tqdm.tqdm(recipes):
      best = complement(recipe_id)
      out.write('%s\t%s\n' % (recipe_id, '\t'.join(best)))


if __name__ == '__main__':
  importall()
  writeToFile(__file__[:-3] + '.txt')
