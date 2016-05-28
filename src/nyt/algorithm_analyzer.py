import os
import analyzers
from random import randint
from collections import defaultdict

anals = [anal for anal in dir(analyzers) if (anal[0] != "_" and anal != "utils" and anal != "analyzer_genPMI")]

print anals

removed = {}
results = defaultdict(int)


mapping = analyzers.utils._getmapping()
top_ingredients = analyzers.utils.gettop()

for filename in os.listdir(analyzers.utils.TEST_DIR):
    ingredients = list(analyzers.utils.get_ingredients(filename, directory=analyzers.utils.TEST_DIR))
    if len(ingredients) == 0:
        continue

    # remove random element that is mapped to top element
    counter = 0
    r = None
    while(counter < len(ingredients)):
        counter += 1
        temp = randint(0, len(ingredients) - 1)
        if ingredients[temp] not in mapping:
            if ingredients[temp] in top_ingredients:
                r = ingredients.pop(temp)
                break
        elif mapping[ingredients[temp]] in top_ingredients:
            r = ingredients.pop(temp)
            break

    # key is filename, value is (removed ingredient, remaining ingredients)
    if r == None:
        continue
    else:
        removed[filename] = (r, ingredients)

print len(removed)

for a in anals:
    print "Running " + a

    analyzers.__dict__[a].importall()

    for filename in removed:
        suggestions = analyzers.__dict__[a].complement(recipe_id = None, 
                    ingredients = removed[filename][1])
        if removed[filename][0] in mapping:
            if mapping[removed[filename][0]] in suggestions:
                results[a] += 1
        else:
            if removed[filename][0] in suggestions:
                results[a] += 1

    print results


