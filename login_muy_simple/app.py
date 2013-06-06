#!../venv/bin/python
from functools import wraps 
from flask import Flask, request, Response 

app = Flask(__name__)

def check_auth(username, password):
	return username == 'admin' and password == 'secret'
	
def authenticate():
	return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated 
	
@app.route('/secret')
@requires_auth
def secret():
	return "Hola loco mundo"	
@app.route('/')
def index():
   return "Hola mundete.!!"


if __name__ == '__main__':
   app.run(debug=True)
