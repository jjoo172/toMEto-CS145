""" Application entry point. Run 
      >> python app.py
    to start the webpage.
"""
import sys

from flask import Flask, render_template, json, request
import nyt.search as search

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

@app.route('/signUp', methods=['POST'])
def signUp():
 
  mylist = []
  counter = 1
    # read the posted values from the UI
    #request.form['myInput' + str(counter)] != true
  while (True):
    try:
      mylist.append(request.form['myInput' + str(counter)])
      print mylist
      print "success"
      counter += 1;
    except:
      break 

  print "ingredients list: "
  for i in mylist:
    print i
    if (i == ""):
      return render_template('index.html')


# Recipe search option
@app.route('/simplesearch', methods=['GET'])
def simplesearch():
  return render_template('simplesearch.html', num_results=0) # initialize num_results to 0, and no content.

@app.route('/simplesearch', methods=['POST'])
def simplesearch_searched():
  searchquery = request.form['simplesearch']

  search_ids = search.search(searchquery)

  # iterate through complements list, adding tuples of (id, list of complements)
  content = []

  for k in search_ids:
    value = [k]
    if k in complements:
      value.append(complements[k])
    else:
      value.append('NULL')

    #content.append('%s: %s' % (k, complements[k] if k in complements else 'NULL'))
    content.append(value)

  print content

  #content = ['%s: %s' % (k, complements[k] if k in complements else 'NULL') for k in search_ids]

  #
  # TODO: separate page for single line errors?
  #

  try:
    search_ids = search.search(searchquery)
  except Exception as e:
    # TODO: better error message
    return render_template('simplesearch_searched.html', query=searchquery,
            content = [['Unable to establish connection to nytimes'], "test"], num_results=1)

  if (len(search_ids) == 0):
    return render_template('no_results.html', query=searchquery, content=content, num_results=0)

  else:
    return render_template('simplesearch_searched.html', query=searchquery, 
            content=content, num_results=len(search_ids)) 


# Loading complementary ingredients
def load(filename):
  global complements
  complements = {}

  with open(filename, 'r') as f:
    for line in f:
      tokens = line.strip().split('\t')
      complements[tokens[0]] = tokens[1:]


# Application entry point
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print 'Need complement file to run'
  else:
    print 'Loading complements . . .'
    load(sys.argv[1])
    print 'Launching webpage . . .'
    app.run()