import os
import re
import tqdm


DL_DIR = 'dls/'
PROCESS_DIR = 'processed/'
DB_DIR = 'db/'



def hasprocessed(filename):
  # Check if recipe already processed
  return os.path.isfile(PROCESS_DIR + filename)


def process(filename):
  # Process and save
  f = open(DL_DIR + filename, 'r')
  content = f.read()
  f.close()

  pattern = r'ingredient-name">.*?<span>(.*?)</span>'
  matches = re.findall(pattern, content)

  f = open(PROCESS_DIR + filename, 'w')
  for m in matches:
    f.write(m + '\n')
  f.close()


# if __name__ == '__main__':
#   # Get all downloaded recipe files
#   allfiles = [f for f in os.listdir(DL_DIR) if os.path.isfile(DL_DIR + f)]

#   # Process all unprocessed recipes
#   for f in tqdm.tqdm(allfiles):
#     if not hasprocessed(f):
#       process(f)


def hasprocessed2(filename):
  # Check if recipe already processed
  return os.path.isfile(DB_DIR + filename)

def process2(filename):
  # Process and save
  f = open(DL_DIR + filename, 'r')
  content = f.read()
  f.close()

  pattern = r'og:title" content="(.*?)"'
  matches = re.findall(pattern, content)
  assert len(matches) == 1
  title = matches[0]

  start = '<div class="recipe-instructions">'
  end = '</div> <!-- /.recipe-instructions -->'
  s = content.find(start)
  e = content.find(end)
  assert s >= 0
  assert e >= 0
  body = content[s:e+len(end)]

  f = open(DB_DIR + filename, 'w')
  f.write(title + '\n' + body)
  f.close()

if __name__ == '__main__':
  # Get all downloaded recipe files
  allfiles = [f for f in os.listdir(DL_DIR) if os.path.isfile(DL_DIR + f)]

  # Process all unprocessed recipes
  for f in tqdm.tqdm(allfiles):
    if not hasprocessed2(f):
      try:
        process2(f)
      except e:
        print 'failed for ' + f
        print e
