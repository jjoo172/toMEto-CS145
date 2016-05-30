import codecs
import os
import re
import tqdm

import allrecipes_mapper


DL_DIR = 'allrecipes_dls/'
TEMP_DIR = 'allrecipes_temp/'
PROCESS_DIR = 'allrecipes_processed/'

MAPPING_FILE = 'nyt_mapper_mapping.txt'
TOP_FILE = 'nyt_mapper_top.txt'

PREFIX = 'allrecipes_'


def extractrecipes():
  """ Read recipes from DL_DIR and write ingredients to TEMP_DIR"""
  # Get all downloaded recipe files
  allfiles = [f for f in os.listdir(DL_DIR) if os.path.isfile(DL_DIR + f)]

  # Process all unprocessed recipes
  for filename in tqdm.tqdm(allfiles):
    # Check if already processed
    if not os.path.isfile(TEMP_DIR + filename):
      # Read in
      f = codecs.open(DL_DIR + filename, 'r', 'utf-8')
      content = f.read()
      f.close()

      # Regex to extract ingredients
      pattern = r'itemprop="ingredients">(.+?)<'
      ingredients = set(re.findall(pattern, content))

      f = codecs.open(TEMP_DIR + filename, 'w', 'utf-8')
      for i in ingredients:
        f.write(i + '\n')
      f.close()

def importrecipes():
  """ Read all recipes from TEMP_DIR"""
  recipes = {}

  # Get all downloaded recipe files
  allfiles = [f for f in os.listdir(TEMP_DIR) if os.path.isfile(TEMP_DIR + f)]

  # Process all unprocessed recipes
  for filename in tqdm.tqdm(allfiles):
    ingredients = set([])

    # Read in
    f = codecs.open(TEMP_DIR + filename, 'r', 'utf-8')
    for line in f:
      line = line.strip().lower()
      if line:
        ingredients |= set([line])
    f.close()

    # Regex to extract ingredients
    recipes[filename] = ingredients

  return recipes

def getmapping():
  """ Loads the ingredient mapping to reduce redundancy. Returns a dict """
  mapping = {}
  with codecs.open(MAPPING_FILE, 'r', 'utf-8') as f:
    for line in f:
      a, b = line.rstrip('\n').split('\t')
      mapping[a] = b
  return mapping

def gettop():
  """ Return a set of the top ingredients (in file specified by TOP_FILE) """
  topset = set([])
  with codecs.open(TOP_FILE, 'r', 'utf-8') as f:
    for line in f:
      topset |= set([line.strip()])
  return topset

def processall(recipes, mapping):
  for r in recipes:
    ingredients = recipes[r]
    ingredients2 = set([])
    for i in ingredients:
      if i in mapping:
        i = mapping[i]
      ingredients2 |= set([i])

    f = codecs.open(PROCESS_DIR + PREFIX + r, 'w', 'utf-8')
    f.write(r + '\n' + '\t'.join(ingredients2) + '\n\n')
    f.close()


if __name__ == '__main__':
  # First extract the ingredients from raw HTML
  extractrecipes()

  # Load ingredients 
  recipes_ = importrecipes()

  # Import the NYT mapping and top set
  nytmap_ = getmapping()
  nyttop_ = gettop()

  # Get a mapping from allrecipes ingredients to NYT ingredients
  allrecipes_mapping = allrecipes_mapper.main(recipes_, nytmap_, nyttop_)

  # Process all recipes
  processall(recipes_, allrecipes_mapping)
