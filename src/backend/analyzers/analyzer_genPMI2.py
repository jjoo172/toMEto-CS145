""" USAGE: 
  >> python analyzer_PMI2.py
"""

import codecs
import os
import tqdm
import heapq
from collections import defaultdict
import numpy as np

import itertools
import utils


def genPMI(s):
    num = len(recipes)
    for pairs in list(itertools.combinations(s,2)):
        num = min(num, graph[pairs[0]][pairs[1]])
    num = num / float(len(recipes))
    denom = 1.0
    for i in s:
        denom *= float(num_recipe[i]) / len(recipes)
    return np.log(num / denom)

def analyze():
    ok = 0
    failed = 0
    for recipe_id in tqdm.tqdm(recipes):
        if "allrecipes" in recipe_id:
            continue
        ingredients = recipes[recipe_id]
        subsets=list(itertools.combinations(ingredients,3))
        bestMatch = ("", float("-inf"))
        for s in subsets:
            pmi = genPMI(s)
            if pmi > bestMatch[1]:
                bestMatch = (s, pmi)
        # print bestMatch, recipe_id
        if bestMatch[1] < -2000:
            failed += 1
        else:
            ok += 1
    print "% num_failed", failed, "/", len(recipes)
    print "% ok", ok, "/", len(recipes)



def importall(recipes_=None):
  """ Call to import everything """
  global graph, degree, recipes, top, num_recipe

  graph = defaultdict(lambda: defaultdict(float))
  degree = defaultdict(float)
  recipes = recipes_ if recipes_ else utils.getrecipes(mapped=True)
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


def sum_of_weights(s):
  res = 0
  for pairs in list(itertools.combinations(s,2)):
    res += graph[pairs[0]][pairs[1]]
  return res



def complement(recipe_id, ingredients=None):
  """ Complement of a recipe """
  if not ingredients:
    ingredients = recipes[recipe_id]
  global d

  d = defaultdict(float)
  top10 = heapq.nlargest(10, degree, key=lambda k: degree[k]) # ignore top 10 ingredients

  maxIngredients = 3
  comb = list(itertools.combinations(ingredients, maxIngredients))
  bestMatch = ((), float("-inf"))
  for s in comb:
      if any(i not in graph for i in s):
        continue
      score = sum_of_weights(s)
      if bestMatch[1] < score:
        bestMatch = (s, score)

  s = bestMatch[0]
  pmi = genPMI(s)
  for a in s:
    for b in graph[a]:
        if b in ingredients:
            continue
        try:
            ing = list(s)
            ing.append(b)
            pmi = genPMI(ing)
        except:
            continue
        if b in d:
            d[b] = max(d[b], pmi)
        else:
            d[b] = pmi

  return heapq.nlargest(10, d, key=lambda k: d[k])


def writeToFile(filename):
  with codecs.open(filename, 'w', 'utf-8') as out:
    for recipe_id in tqdm.tqdm(recipes):
      best = complement(recipe_id)
      out.write('%s\t%s\n' % (recipe_id, '\t'.join(best)))


if __name__ == '__main__':
  importall()
  writeToFile(__file__[:-3] + '.txt')
