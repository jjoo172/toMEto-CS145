import os
import re
import tqdm


PROCESS_DIR = 'processed/'
PROCESS_DIR_2 = 'processed2/'
PREFIX = 'allrecipes_'


def hasprocessed(filename):
  # Check if recipe already processed
  return os.path.isfile(PROCESS_DIR + filename)


def process(filename):
  # Process and save
  f = open(PROCESS_DIR + filename, 'r')
  content = f.read()
  f.close()

  pattern = r'itemprop="ingredients">(.+?)<'
  matches = re.findall(pattern, content)

  f = open(PROCESS_DIR + filename, 'w')
  for m in matches:
    f.write(m + '\n')
  f.close()


if __name__ == '__main__':
  # Get all downloaded recipe files
  allfiles = [f for f in os.listdir(PROCESS_DIR) if os.path.isfile(PROCESS_DIR + f)]

  # Process all unprocessed recipes
  for f in tqdm.tqdm(allfiles):
    process(f)
