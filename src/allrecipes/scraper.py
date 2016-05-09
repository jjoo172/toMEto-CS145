import os.path
import re
import sys
import time
import urllib2
from tqdm import trange


MAX_QUEUE_SIZE = 100000 
NUM_DL = 1
WAIT_DELAY = 1
QUEUE_FILE = 'queue.txt'
DL_DIR = 'dls/'
BASE_URL = 'http://allrecipes.com/'


def httpget(url):
  # HTTP GET request the url, return contents.
  req = urllib2.urlopen(url)
  content = req.read()
  req.close()
  return content


def saveQueue(queue):
  # Save queue to file
  f = open(QUEUE_FILE, 'w')
  for q in queue:
    f.write(q + '\n')
  f.close()


def loadQueue():
  # Load queue from file
  f = open(QUEUE_FILE, 'r')
  queue = set([])
  for line in f:
    queue |= set([line.strip()])
  f.close()
  return queue


def hasrecipe(recipe_id):
  # Check if recipe already downloaded
  return os.path.isfile(DL_DIR + recipe_id + '.txt')


def saverecipe(recipe_id, content):
  # Save recipe
  f = open(DL_DIR + recipe_id + '.txt', 'w')
  f.write(content)
  f.close()


def getNewIds(content):
  # Return a set of valid recipe ids
  pattern = r'<a href="/recipe/(\d+)/'
  matches = re.findall(pattern, content)
  newids = set([])
  for m in matches:
    if not hasrecipe(m):
      newids |= set([m])
  return newids


if __name__ == '__main__':

  # contents = httpget('http://allrecipes.com/recipes/?sort=newest')
  # queue = loadQueue() | getNewIds(contents)
  # saveQueue(queue)

  # First argument is amount of downloads to do, else default 1
  if len(sys.argv) > 1:
    NUM_DL = int(sys.argv[1])

  # Fetch recipe queue
  queue = loadQueue()

  for _ in trange(NUM_DL):
    # Get an id that has not been downloaded yet
    recipe_id = queue.pop()
    while hasrecipe(recipe_id):
      recipe_id = queue.pop()

    # Download and save recipe
    try:
      content = httpget(BASE_URL + 'recipe/' + recipe_id)
      saverecipe(recipe_id, content)
      if len(queue) < MAX_QUEUE_SIZE:
        queue |= getNewIds(content)
    except Exception as e:
      print 'Error while retrieving recipe: ' + recipe_id
      print e
      time.sleep(WAIT_DELAY * 100)

    # Sleep to avoid throttling
    time.sleep(WAIT_DELAY)
    saveQueue(queue)
