from flask import Flask, render_template, json, request
app = Flask(__name__)

@app.route("/")
def main():
	print "eieie"
	return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
	print "asdfasdf"
	return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
 
    # validate the received values
    if _name and _email and _password:
    	print "tite"
        return json.dumps({'html':'<span>All fields good !!</span>'})

    else:
    	print "not all things filled in"
        return json.dumps({'html':'<span>Enter the required fields</span>'})
      

if __name__ == "__main__":
	print "aaaaa"
	app.run()


	