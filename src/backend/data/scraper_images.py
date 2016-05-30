import os
import re
import tqdm
import urllib2
import time


WAIT_DELAY = 2
DL_DIR = 'dls/'
IMG_DIR = 'images/'


def httpget(url):
  # HTTP GET request the url, return contents.
  req = urllib2.urlopen(url)
  content = req.read()
  req.close()
  return content


def hasprocessed(filename):
  # Check if recipe already processed
  return os.path.isfile(IMG_DIR + filename)


def process(filename):
  # Process and save
  f = open(DL_DIR + filename, 'r')
  content = f.read()
  f.close()

  pattern = r'og:image" content="(.*?)"/>'
  matches = re.findall(pattern, content)

  assert len(matches) == 1
  m = matches[0]

  if 'static/images/pattern' in m:
    return False

  if '.png' in m:
    ext = '.png'
  elif '.jpg' in m:
    ext = '.jpg'
  elif '.jpeg' in m:
    ext = '.jpeg'
  else:
    print m
    return False

  image_filename = IMG_DIR + filename[:-4] + ext
  if not hasprocessed(image_filename):
    f = open(image_filename, 'wb')
    f.write(httpget(m))
    f.close()
    return True

  return False


if __name__ == '__main__':
  # Get all downloaded recipe files
  allfiles = [f for f in os.listdir(DL_DIR) if os.path.isfile(DL_DIR + f)]

  # Process all unprocessed recipes
  count = 0
  for f in tqdm.tqdm(allfiles):
    # Download and save image
    try:
      if process(f):
        # Sleep to avoid throttling
        time.sleep(WAIT_DELAY)
    except Exception as e:
      print 'Error while retrieving: ' + f
      print e
      time.sleep(WAIT_DELAY * 100)
