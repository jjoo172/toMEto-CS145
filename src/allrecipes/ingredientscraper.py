import re
import time
import urllib2


FILE_STORAGE = 'ingredients.txt'
WAIT_DELAY = 2
BASE_URL = 'http://www.food.com/about/?pn='


def httpget(url):
  # HTTP GET request the url, return contents.
  req = urllib2.urlopen(url)
  content = req.read()
  req.close()
  return content


def getingredients(content):
  # Return a set of valid recipe ids
  pattern = r'"title":"(.+?)"'
  matches = re.findall(pattern, content)
  return matches


def dl():
  ingredients = set([])
  for i in xrange(1, 100):
    try:
      content = httpget(BASE_URL + str(i))
      newingredients = getingredients(content)
      print newingredients
      ingredients |= set(newingredients)
    except Exception as e:
      print 'Error for ' + str(i)
      print e
    time.sleep(WAIT_DELAY)

  with open(FILE_STORAGE, 'w') as f:
    for i in ingredients:
      f.write(i + '\n')

def load():
  ingredients = set([])
  with open(FILE_STORAGE, 'r') as f:
    for line in f:
      ingredients |= set([line.strip().lower()])
  return ingredients
