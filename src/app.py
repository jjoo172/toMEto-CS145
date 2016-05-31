""" Application entry point. Run 
      >> python app.py
    to start the webpage.
"""
import sys
import os

from flask import Flask, render_template, json, request
import backend.search as search
import backend.analyzers.utils as utils

app = Flask(__name__)


# Home page
@app.route("/")
def main():
  return render_template('simplesearch.html', num_results=0)

@app.route("/index")
def index():
  return render_template('index.html')


# Enter ingredients option
@app.route('/ingredients')
def ingredients():
  return render_template('ingredients.html')

# Recipe search option
@app.route('/simplesearch', methods=['GET'])
def simplesearch():
  return render_template('simplesearch.html', num_results=0) # initialize num_results to 0, and no content.

@app.route('/simplesearch', methods=['POST'])
def simplesearch_searched():
  searchquery = request.form['simplesearch']

  try:
    search_ids = search.search(searchquery)
  except Exception as e:
    # TODO: better error message, current one does not work
    return render_template('no_results.html', query=searchquery)
    # return render_template('simplesearch_searched.html', query=searchquery,
    #         content = [['Unable to establish connection to nytimes', "We apologize for the inconvenience"]], num_results=1)

  if (len(search_ids) == 0):
    return render_template('no_results.html', query=searchquery)

  else:

    # iterate through complements list, adding tuples of (id, list of complements)
    content = []

    for k in search_ids:
      try:
        title, body = utils.getrecipe_info(k)
        image = getrecipeimage(k)

        value = [k]
        if k in complements:
          complements_list = [n.capitalize() for n in complements[k]] #capitalize first letter
        else:
          complements_list = 'NULL'

        content.append([k, complements_list, title, body, image])

      except:
        pass

    return render_template('simplesearch_searched.html', query=searchquery, 
            content=content, num_results=len(content)) 


# Loading complementary ingredients
def load(filename):
  global complements
  complements = {}

  with open(filename, 'r') as f:
    for line in f:
      tokens = line.strip().split('\t')
      complements[tokens[0]] = tokens[1:]


#getting ingredients images
def getrecipeimage(recipe_id): 
  location = 'static/img/recipes/' + recipe_id + '.jpg'
  if os.path.isfile(location): 
    return '../' + location 
  else: 
    return "../static/img/transparent.png"

# Application entry point
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print 'Need complement file to run'
  else:
    print 'Loading complements . . .'
    load(sys.argv[1])
    print 'Launching webpage . . .'
    app.run()