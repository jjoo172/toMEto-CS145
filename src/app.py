from flask import Flask, render_template, json, request
import nyt.search as search

app = Flask(__name__)
LIMIT = 10

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/index")
def index():
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')


@app.route('/simplesearch')
def simplesearch():
	return render_template('simplesearch.html', num_results=0) # initialize num_results to 0, and no content.

@app.route('/searchQuery', methods=['POST'])
def searchQuery():
	searchquery = request.form['searchQuery']
	print searchquery
	search_ids = search.search(searchquery)
	print search_ids
	return render_template('simplesearch_searched.html', content=search_ids, num_results=len(search_ids)) #num_results will be returned by the function which lists recipes!


@app.route('/landing')
def landing():
	return render_template('landing.html')
"""
@app.route('/landingSignUp', methods=['POST'])
def landingSignUp():
	print "asdf"
	search_query = request.form['search_input']
	print search_query
	print "success"
"""



@app.route('/landing2')
def landing2():
	return render_template('landing2.html')

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
	 

    # validate the received values
	#if _ing1 and _ing2 and _ing3:
#		print "tite"
#		return json.dumps({'html':'<span>All fields good !!</span>'})
#
#	else:
#		print "not all things filled in"
#		return json.dumps({'html':'<span>Enter the required fields</span>'})
      

if __name__ == "__main__":
	print "Launching webpage:"
	app.run()


	