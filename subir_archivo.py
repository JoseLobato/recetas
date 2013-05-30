#!venv/bin/python


import os 
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

# ruta completa a la carpeta en donde se guardaran los ficheros
UPLOAD_FOLDER = '/home/jose/Escritorio/myproject/archivos' 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file', filename=filename))
									
	return """
	<!doctype html>
	<html>
		<head>
			<title>Upload new File</title>	
		</head>
			<h1>Upload new File</h1>
			<form action="" method="post" enctype="multipart/form-data">
			<div id="uploader">
			    <p><input type="file" name="file"></p>
				<input type="submit" value="Upload">
			</div>
			</form>
	</html>
	"""
@app.route('/uploads/<filename>')
def uploaded_file(filename):  # muestra el fichero en el navegador
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	
if __name__ == '__main__':
	app.run(debug=True)			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
