""" Objective compare the analyzers.

1. Sort recipes into training and test sets. (Only NYT recipes can go into test set)
2. Remove NUM_REMOVED ingredients from each of the recipes in the test set. 
   Only "top" ingredients can be removed since analyzers predict only those.
3. Run the complement() function on the altered recipe.
4. For each removed ingredient that is recommended, +1 score.

"""
import os
import analyzers
import random
from collections import defaultdict


TEST_SET_PERCENTAGE = 0.2
NUM_REMOVED = 1


# Store removed ingredients and final results
removed = {}
results = defaultdict(int)


# All recipes, top ingredients, training set, and test set
recipes = analyzers.utils.getrecipes(mapped=True)
top = analyzers.utils.gettop()
trainingset = {}
testset = {}


# Sort recipes into training and test sets
for recipe_id in recipes:
  if 'allrecipes' not in recipe_id and random.random() < TEST_SET_PERCENTAGE:
    testset[recipe_id] = recipes[recipe_id]
  else:
    trainingset[recipe_id] = recipes[recipe_id]


# Remove ingredients (restricted to within the top set)
to_del = set([])
for recipe_id in testset:
  # Get the top ingredients in the recipe (these are candidates for removal)
  top_ingredients = set([])
  for i in testset[recipe_id]:
    if i in top:
      top_ingredients |= set([i])

  # Get the maximum amount of ingredients to remove
  num_to_remove = min(NUM_REMOVED, len(top_ingredients))

  # Sample and remove
  to_remove = random.sample(top_ingredients, num_to_remove)
  testset[recipe_id] -= set(to_remove)
  removed[recipe_id] = to_remove

  # If empty ingredients, then mark for deletion from testset
  if not testset[recipe_id]:
    to_del |= set([recipe_id])


# Purge empty recipes
for recipe_id in to_del:
  del testset[recipe_id]
  del removed[recipe_id]


# Test on all analyzers
anals = [anal for anal in dir(analyzers) if (anal[0] != "_" and anal != "utils" and anal != "analyzer_genPMI")]
print 'anals:', anals
print 'len(testset):', len(testset)
for a in anals:
  print "Running " + a

  # Run on training set only
  analyzers.__dict__[a].importall(trainingset)

  for recipe_id in testset:
    # Get suggestions on altered set
    suggestions = analyzers.__dict__[a].complement(recipe_id=None, ingredients=testset[recipe_id])
    
    # Run through removed ingredients and check if they are present
    for r in removed[recipe_id]:
      if r in suggestions:
        results[a] += 1

  print results
