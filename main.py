import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS,cross_origin
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'E:/Uploads'

app = Flask(__name__)
CORS(app)
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/multiple-files-upload', methods=['POST', 'GET','OPTIONS'])
@cross_origin(supports_credentials=True)
def upload_file():
	# check if the post request has the file part
	#print("request.data", request.data)

	#fileStorage = request.files['file']
	#print('FileStorage ', fileStorage)
	print('request files  ', request.files)
	print('request.form ', request.form)
	print('request.args ', request.args)
	print('request.json ', request.json)

	#if 'files[]' not in request.files:
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp

	#files = request.files.getlist('files[]')
	files = request.files.getlist('file')

	errors = {}
	success = False

	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			success = True
		else:
			errors[file.filename] = 'File type is not allowed'

	if success and errors:
		errors['message'] = 'File(s) successfully uploaded'
		resp = jsonify(errors)
		resp.status_code = 500
		return resp
	if success:
		resp = jsonify({'message' : 'Files successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify(errors)
		resp.status_code = 500
		return resp

if __name__ == "__main__":
    app.run()
