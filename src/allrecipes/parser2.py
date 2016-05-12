import os
import re
import tqdm

import utils


PROCESS_DIR = 'processed/'
PROCESS_DIR_2 = 'processed2/'
PREFIX = 'allrecipes_'


def hasprocessed(filename):
  # Check if recipe already processed
  return os.path.isfile(PROCESS_DIR + filename)


def process(r):
  ingredients = recipes[r]
  ingredients2 = set([])
  for i in ingredients:
    if i in mapping:
      i = mapping[i]
    ingredients2 |= set([i])

  f = open(PROCESS_DIR_2 + PREFIX + r + '.txt', 'w')
  for i in ingredients2:
    f.write(i + '\n')
  f.close()


if __name__ == '__main__':
  global mapping, recipes
  mapping = utils._getmapping2()
  recipes = utils.getrecipes()

  # Process all unprocessed recipes
  for r in tqdm.tqdm(recipes):
    process(r)
