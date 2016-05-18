import os
import analyzers
from random import randint
from collections import defaultdict

anals = [anal for anal in dir(analyzers) if (anal[0] != "_" and anal != "utils" and anal != "analyzer_genPMI")]

print anals

removed = {}
results = defaultdict(int)

for filename in os.listdir(analyzers.utils.TEST_DIR):
    ingredients = list(analyzers.utils.get_ingredients(filename, directory=analyzers.utils.TEST_DIR))
    if len(ingredients) == 0:
        continue

    # remove random element
    temp = randint(0,len(ingredients) - 1)
    r = ingredients.pop(temp)

    removed[filename] = (r, ingredients)

for a in anals:
    print "Running " + a

    analyzers.__dict__[a].importall()

    for filename in removed:
        suggestions = analyzers.__dict__[a].complement(recipe_id = None, 
                    ingredients = removed[filename][1])
        if removed[filename][0] in suggestions:
            results[a] += 1

    print results


print results

