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
  content = ['%s: %s' % (k, complements[k] if k in complements else 'NULL') for k in search_ids]

  # print searchquery
  # print search_ids
  # print content

  #num_results will be returned by the function which lists recipes!

  # no searches match.
  if (len(search_ids) == 0):
    return render_template('no_results.html')

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