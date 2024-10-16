from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Manan@2303'
app.config['MYSQL_DB'] = 'Assignment7'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	msg = request.args.get('msg', '')
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM Users WHERE username = % s \
			AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['username'] = account['username']
			msg = 'Logged in successfully!'
			return render_template('index.html', msg=msg, username=session['username'])
		else:
			msg = 'Incorrect Username / Password!'
	return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		mobile = request.form['mobile']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute(
			'SELECT * FROM Users WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists!'
		else:
			cursor.execute('INSERT INTO Users VALUES \
			(NULL, % s, % s, % s)',
						(username, mobile,password ))
			mysql.connection.commit()
			msg = 'You have successfully registered!'
			return redirect(url_for('login', msg=msg))
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg=msg)


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html",username=session['username'])
	return redirect(url_for('login'))
