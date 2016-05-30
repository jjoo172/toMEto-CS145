""" USAGE: 
  >> python analyzer_naive.py
"""

import codecs
import tqdm
import heapq
from collections import defaultdict

import utils


def importall(recipes_=None):
  """ Call to import everything """
  global graph, degree, recipes, top

  graph = defaultdict(lambda: defaultdict(float))
  degree = defaultdict(float)
  recipes = recipes_ if recipes_ else utils.getrecipes()
  top = utils.gettop()

  for recipe_id in tqdm.tqdm(recipes):
    ingredients = recipes[recipe_id]

    for a in ingredients:
      for b in ingredients:
        if a != b and a in top and b in top:
          graph[a][b] += 1.0

  for a in graph:
    for b in graph[a]:
      degree[a] += graph[a][b]


def complement(recipe_id, ingredients=None):
  """ Complement of a recipe """
  if not ingredients:
    ingredients = recipes[recipe_id]

  d = defaultdict(float)
  top10 = heapq.nlargest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients
  for i in ingredients:
    if i in graph and i not in top10:
      for k in graph[i]:
        if k in ingredients or k in top10:
          continue

        d[k] += min(graph[i][k]/degree[i], graph[k][i]/degree[k])

  return heapq.nlargest(10, d, key=lambda k: d[k])


def writeToFile(filename):
  with codecs.open(filename, 'w', 'utf-8') as out:
    for recipe_id in tqdm.tqdm(recipes):
      best = complement(recipe_id)
      out.write('%s\t%s\n' % (recipe_id, '\t'.join(best)))


if __name__ == '__main__':
  importall()
  writeToFile(__file__[:-3] + '.txt')
