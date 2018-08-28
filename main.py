from search import search
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import MySQLdb

app =Flask(__name__)
app.secret_key = 'movehack2018'

@app.route('/sign-up', methods = ['GET', 'POST'])
def signup():
	if request.method == 'GET' :
		return render_template('sign-up.html')

	username = request.form['username']
	password = request.form['password']
	flag = request.form.get('flag')
	query = 'insert into user(username, password, flag) values( %s, %s, %s)'
	db = dbconnect()
	cur = db.cursor()
	cur.execute(query,(username, password, flag))
	db.commit()
	db.close()
	return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():	

	if request.method == 'POST':
	
		username = request.form['username']
		password = request.form['password']
		db = dbconnect()
		cur = db.cursor()
		#query = 'SELECT * FROM user WHERE username==\'' + str(username) + '\' AND password==\'' + str(password) + '\'' 
		query = 'SELECT * FROM user WHERE username=%s AND password=%s'
		cur.execute(query,(username,password))
		for row in cur.fetchall() :
			session['username'] = request.form['username']
			if int(row[3]) == 1:
				return render_template('atc_homepage.html', flag=1)
			else : 
				return render_template('do_homepage.html', flag=0)
		db.close()
	return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	# remove the username from the session if it is there
	session.pop('username', None)
	return render_template('index.html')


@app.route('/')
def index():
	if 'username' in session : 
		username = session['username']

		db = dbconnect()
		cur = db.cursor()
		query = 'SELECT flag FROM user WHERE username=%s'
		cur.execute(query,[username])
		for row in cur.fetchall():
		    if int(row[0]) == 1 :
		    	return render_template('atc_homepage.html', flag=1)
		    else : 
		    	return render_template('do_homepage.html', flag=0)

		db.close()

	else : 
		#login()
		return render_template('index.html')

def dbconnect() : 
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="movehack",         # your username
                     passwd="movehack",  # your password
                     db="dutms")        # name of the data base
	return db

@app.route('/askForRoute', methods = ['GET', 'POST'])
def askForRoute():
	return render_template('choose_path.html')

@app.route('/viewDroneDetails')
def view_drone_details():
	flag=0
	return render_template('view_drone_details.html', flag=flag)

@app.route('/getDroneDetails', methods =['GET', 'POST'])
def getDroneDetails():
	drone_id = request.form['drone_id']
	drone_dict = {}
	db = dbconnect()
	cur = db.cursor()
	query = 'select * from drone where drone_id=%s'
	cur.execute(query,[drone_id])
	for row in cur.fetchall():

		drone_dict['drone_id'] = row[0]
		drone_dict['drone_name'] = row[1]
		drone_dict['start_point'] = row[2]
		drone_dict['end_point'] = row[3]
		drone_dict['start_time'] = row[4]
		drone_dict['end_time'] = row[5]

	db.close()
	flag=1
	return render_template('view_drone_details.html',flag=flag, drone_dict=drone_dict)
	

@app.route('/getRoutePlan', methods = ['GET', 'POST'])
def routePlan():

	if request.method == 'POST' :
		drone_id = request.form['drone_id']
		drone_name = request.form['drone_name']
		start_point = request.form['start_point']
		end_point = request.form['end_point']
		start_time = request.form['start_time']
		end_time = request.form['end_time']
		db = dbconnect()
		cur = db.cursor()
		query = 'insert into drone values(%s, %s, %s, %s, %s, %s)'		
		cur.execute(query,(drone_id, drone_name, start_point, end_point, start_time, end_time))
		db.commit()
		db.close()
		sp = start_point.split(' ')
		ep = end_point.split(' ')
		route_path = search(int(sp[0]),int(sp[1]),int(ep[0]),int(ep[1]))
		two_d_matrix = []
		length = 20
		height = 20
		for y in range(length):
			board_matrix = []
			for x in range(height):
				val = str(route_path.theboard.squares[x][y])
				if val == '0' :
					board_matrix.append(' ')
				else:
					board_matrix.append(val)
			two_d_matrix.append(board_matrix)

		return render_template('possible_paths.html', two_d_matrix=two_d_matrix, x=30, y=30)

if __name__ == '__main__' :
	app.debug = True
	app.run()