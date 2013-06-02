
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, g, render_template, redirect, url_for, session, \
request, _app_ctx_stack, flash 
from werkzeug import check_password_hash, generate_password_hash

# configuracion 
DATABASE = 'users.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'acahayqueponeralgomuydificildeadivinar'


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db
    
def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv
    
def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)
  
  
                          
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html')
	
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user:
		return redirect(url_for('index'))
	error = None
	if request.method == 'POST':
		user = query_db("""select * from user where
            username = ?""", [request.form['username']], one=True)
		if user is None:
			error = 'Nombre de usuario incorrecto.'
		elif not check_password_hash(user['pw_hash'], request.form['password']):
			error = u'La contrasena es incorrecta.'
		else:
			flash('Usted ha iniciado session.')	
			session['user_id'] = user['user_id']
			return redirect(url_for('index'))
	return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if g.user:
		return redirect(url_for('index'))
	error = None 
	if request.method == 'POST':
		if not request.form['username']:
			error = "Tienes que escribir tu nombre de usuario."
		elif not request.form['email'] or '@' not in request.form['email']:
			error = 'Su email es incorrecto.'
		elif not request.form['password']:
			error = 'Usted no ingreso su password.'
		elif request.form['password'] != request.form['password2']:
			error = 'Los dos password no coinciden.'
		elif get_user_id(request.form['username']) is not None:
			error = 'El nombre de usuario ya esta en uso.'
		else:
			db = get_db()
			db.execute(""" insert into user (
					username, email, pw_hash) values (?, ?, ?) """,
					[request.form['username'], request.form['email'],
					generate_password_hash(request.form['password'])])
			db.commit()
			flash('Usted fue registrado con exito y puede iniciar sesion ahora')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    flash('Usted ha cerrado sesion.')
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)
