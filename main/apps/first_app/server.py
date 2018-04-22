from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt  
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "keepitopen"
mysql = connectToMySQL('new_reg')
bcrypt = Bcrypt(app) 

@app.route('/')
def index():
	return render_template('login_reg.html')

@app.route('/process', methods=['POST'])
def submit():
	session['first_name'] = request.form['first_name']
	session['last_name'] = request.form['last_name']
	session['Email'] = request.form['Email']
	password = request.form['password']
	con_pass = request.form['con_pass']
	# query_val = "SELECT email FROM registration WHERE first_name = %(email)s"
	# data = {'email': request.form['email']}
	if len(session['first_name']) == 0:
		flash('please enter your FIRST name')
		print('works?')
		return redirect('/')
	elif len(session['first_name']) < 2:
		flash('your FIRST name needs to be more than 2 characters')
		return redirect('/')
	elif str.isalpha(session['first_name']) == False:
		flash('please enter letters only for your FIRST name')
		return redirect('/')
	elif len(session['last_name']) == 0:
		flash('please enter your LAST name')
		return redirect('/')
	elif len(session['last_name']) < 2:
		flash('your last name needs to be more than 2 characters')
		return redirect('/')
	elif str.isalpha(session['last_name']) == False:
		flash('please enter letters only for your LAST name')
		return redirect('/')
	elif len(session['Email']) == 0:
		flash('please enter your Email')
		return redirect('/')
	elif not EMAIL_REGEX.match(session['Email']):
		flash("Invalid Email Address")
		return redirect('/')
	elif len(password) == 0:
		flash('please enter your password')
		return redirect('/')
	elif len(password) <8 :
		flash('please enter 8 or more characters for your password')
		return redirect('/')
	elif len(con_pass) == 0:
		flash('please confirm your password')
		return redirect('/')
	elif password != con_pass :
		flash('please RETYPE your password for confirmation')
		return redirect('/')
	else:
		print('pw_hash')
		pw_hash = bcrypt.generate_password_hash(request.form['password'])  
		query = "INSERT INTO new_table (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password_hash)s);"
		# session['first_name'] = request.form['first_name']
		# session['last_name'] = request.form['last_name']
		# session['Email'] = request.form['Email']
		# session['password'] = request.form['password']
		# session['con_pass'] = request.form['con_pass']		
		data = {
			'first_name' : request.form['first_name'],
			'last_name' : request.form['last_name'],
			'email' : request.form['Email'],
			'password_hash' : pw_hash 
		}
		print(pw_hash)
    # mysql.query_db(query, data)
    # return redirect("/")
		mysql.query_db(query, data)
		return redirect('/success')


@app.route('/success')
def success():
	# session['first_name'] = request.form['first_name']
	query="SELECT * FROM new_table WHERE first_name = %(first_name)s;"
	print(query)
	return render_template('success.html')




# @app.route('/createUser', methods=['POST'])
# def create():
# 	pw_hash = bcrypt.generate_password_hash(request.form['password'])  
# 	query = "INSERT INTO users (email, password) VALUES (%(email)s, %(password_hash)s);"  
# 	data = { "email" : request.form['email'],
#              "password_hash" : pw_hash }
#     mysql.query_db(query, data)
# return redirect('/')

# need to loggin in order to  
@app.route('/login', methods=['POST'])
def login():
	query="SELECT * FROM new_table WHERE email = %(email)s;"
	data = {'email' : request.form['log_email']}
	result = mysql.query_db(query,data)
	if result:
		if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
			session['Email'] = result[0]['id']
			return redirect('/success')
	else:
		flash('not existed')
	return redirect('/')


@app.route('/logout')
def logout():
	flash('You have been logged OUT!')
	session['first_name'] = ''
	session['last_name'] = ''
	session['Email'] = ''
	password = ''
	con_pass = ''
	return render_template('login_reg.html')


#route
# success 
# login
# password

if __name__=="__main__":
	app.run(debug=True)