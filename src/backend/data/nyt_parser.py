import codecs
import os
import re
import tqdm


DL_DIR = 'nyt_dls/'
PROCESS_DIR = 'nyt_processed/'



def hasprocessed(filename):
  # Check if recipe already processed
  return os.path.isfile(PROCESS_DIR + filename)


def process(filename):
  # Process and save
  f = codecs.open(DL_DIR + filename, 'r', 'utf-8')
  file_content = f.read()
  f.close()

  # Regex to extract title
  title_regex = r'og:title" content="(.*?)"'
  title = re.findall(title_regex, file_content)
  assert len(title) == 1
  title = title[0]
  
  # Regex to extract ingredients
  ingredient_regex = r'ingredient-name">.*?<span>(.*?)</span>'
  ingredients = re.findall(ingredient_regex, file_content)
  ingredients = '\t'.join(ingredients)

  # Extract recipe body
  start = '<div class="recipe-instructions">'
  end = '</div> <!-- /.recipe-instructions -->'
  s = file_content.find(start)
  e = file_content.find(end)
  assert s >= 0
  assert e >= 0
  mid1 = '</ul>'
  mid2 = '</section> <!-- /.recipe-ingredients -->'
  m1 = file_content.find(mid1, s, e)
  m2 = file_content.find(mid2, s, e)
  assert m1 >= 0
  assert m2 >= 0
  body = file_content[s:m1 + len(mid1)] + file_content[m2:e+len(end)]

  # Write to file
  f = codecs.open(PROCESS_DIR + filename, 'w', 'utf-8')
  f.write(title + '\n' + ingredients + '\n' + body)
  f.close()


if __name__ == '__main__':
  # Get all downloaded recipe files
  allfiles = [f for f in os.listdir(DL_DIR) if os.path.isfile(DL_DIR + f)]

  # Process all unprocessed recipes
  for f in tqdm.tqdm(allfiles):
    if not hasprocessed(f):
      process(f)
