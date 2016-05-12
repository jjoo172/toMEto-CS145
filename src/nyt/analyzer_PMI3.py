""" USAGE: 
  >> python analyzer_PMI3.py
"""

import os
import tqdm
import heapq
from collections import defaultdict
import numpy as np

import utils
utils.PROCESS_DIR = 'processed2/'   # Use combined dataset


def PMI(a, b):
    return np.log(graph[a][b] / len(recipes) /\
            (num_recipe[a] / len(recipes) * num_recipe[b] / len(recipes)))


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
      if a in top:
        num_recipe[a] += 1.0;
        for b in ingredients:
          if a != b and b in top:
            graph[a][b] += 1.0

  for a in graph:
    for b in graph[a]:
      degree[a] += PMI(a, b)


def complement(recipe_id):
  """ Complement of a recipe """
  ingredients = recipes[recipe_id]

  score = defaultdict(float)
  count = defaultdict(int)
  for a in ingredients:
    if a in graph:
      for b in graph[a]:
        if b in ingredients:
          continue
        count[b] += 1
        score[b] += PMI(a, b)

  return heapq.nlargest(10, score, key=lambda k: count[k] * score[k])


def writeToFile(filename):
  with open(filename, 'w') as out:
    for recipe_id in tqdm.tqdm(recipes):
      best = complement(recipe_id)
      out.write('%s\t%s\n' % (recipe_id, '\t'.join(best)))


if __name__ == '__main__':
  importall()
  writeToFile(__file__[:-3] + '.txt')
