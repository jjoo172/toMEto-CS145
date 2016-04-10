import os
import re
import tqdm


DL_DIR = 'dls/'
PROCESS_DIR = 'processed/'



def hasprocessed(filename):
  # Check if recipe already processed
  return os.path.isfile(PROCESS_DIR + filename)


def process(filename):
  # Process and save
  f = open(DL_DIR + filename, 'r')
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
  allfiles = [f for f in os.listdir(DL_DIR) if os.path.isfile(DL_DIR + f)]

  # Process all unprocessed recipes
  for f in tqdm.tqdm(allfiles):
    if not hasprocessed(f):
      process(f)
