#!flask/bin/python

from functools import wraps
from flask import Flask, request, redirect, render_template, session, url_for, flash

app = Flask(__name__)
app.secret_key = 'xD\xc7\x0b\xa02\xf2bj\x15\xcd\xd4\xb7\xee2\x1a\xa9\xcb\xeb\xc7-\x91\x89\xbc'


def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('Usted tiene que identificarse.')
			return redirect(url_for('login'))
	return wrap	
	
	
@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')
	
	

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = "Sus datos son invalidos. Por favor intententelo otra vez."
		else:
			session['logged_in'] = True
			return redirect(url_for('index'))
	return render_template('login.html', error=error)
	

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Usted ha cerrado la sesion')
	return redirect(url_for('login'))
	


if __name__ == '__main__':
	app.run(debug=True)
	
	
