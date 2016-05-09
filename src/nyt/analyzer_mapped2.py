""" USAGE: 
  >> python analyzer_mapped2.py
"""

import os
import tqdm
import heapq
from collections import defaultdict

import utils


def importall():
  """ Call to import everything """
  global graph, degree, recipes, top

  graph = defaultdict(lambda: defaultdict(float))
  degree = defaultdict(float)
  recipes = utils.getrecipes(mapped=True)
  top = utils.gettop()

  for recipe_id in tqdm.tqdm(recipes):
    ingredients = recipes[recipe_id]

    for a in ingredients:
      for b in ingredients:
        if a != b and a in top and b in top:
          graph[a][b] += 1.0

  for g in graph:
    for z in graph[g]:
      degree[g] += graph[g][z]


def complement(recipe_id):
  """ Complement of a recipe """
  ingredients = recipes[recipe_id]

  d = defaultdict(float)
  top10 = heapq.nlargest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients
  for a in ingredients:
    if a in graph and a not in top10:
      for b in graph[a]:
        if b in ingredients or b in top10:
          continue
        d[b] += min(graph[a][b]/degree[a], graph[b][a]/degree[b])

  return heapq.nlargest(10, d, key=lambda k: d[k])


def writeToFile(filename):
  with open(filename, 'w') as out:
    for recipe_id in tqdm.tqdm(recipes):
      best = complement(recipe_id)
      out.write('%s\t%s\n' % (recipe_id, '\t'.join(best)))


if __name__ == '__main__':
  importall()
  writeToFile(__file__[:-3] + '.txt')
