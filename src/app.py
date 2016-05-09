""" Application entry point. Run 
      >> python app.py
    to start the webpage.
"""
from flask import Flask, render_template, json, request
import nyt.search as search

app = Flask(__name__)


# Home page
@app.route("/")
def main():
  return render_template('index.html')

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
@app.route('/simplesearch')
def simplesearch():
  return render_template('simplesearch.html', num_results=0) # initialize num_results to 0, and no content.

@app.route('/searchQuery', methods=['POST'])
def searchQuery():
  searchquery = request.form['searchQuery']
  print searchquery
  search_ids = search.search(searchquery)
  print search_ids
  print len(search_ids)
  return render_template('simplesearch_searched.html', content=search_ids, num_results=len(search_ids)) #num_results will be returned by the function which lists recipes!


# Application entry point
if __name__ == "__main__":
  print "Launching webpage:"
  app.run()
