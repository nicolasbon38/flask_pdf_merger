#!/usr/bin/env python3


from flask import Flask, render_template, send_file, flash,request, redirect, url_for
from werkzeug.utils import secure_filename

import os
from pdfrw import PdfReader, PdfWriter

import webbrowser


UPLOAD_FOLDER='./uploads/'

#Si par malheur le dossier uploadds n'existe poas, il faut le créer
if not os.path.exists('./uploads/'):
    os.makedirs('./uploads/')

ALLOWED_EXTENSIONS = {'pdf'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def list_uploaded_files():
    uploaded_files = []
    for file_name in os.listdir('./uploads/'):
        uploaded_files.append(file_name)
    return uploaded_files

#Page home
@app.route('/', methods=['GET'])

def home():    
    return render_template("home.html")


#page fusion
@app.route('/fusion', methods=['GET'])

def merge():
    writer = PdfWriter()
    files = [x for x in os.listdir('uploads') if x.endswith('.pdf')]
    for fname in sorted(files):
        writer.addpages(PdfReader(os.path.join('uploads', fname)).pages)
    writer.write("output.pdf")
    #On supprime les fichiers stockés en local
    files = os.listdir('./uploads/')
    for f in files:
        os.remove('./uploads/' + f)
    return render_template("fusion.html")

#Page download
@app.route('/download', methods=['GET'])

def download():
    return send_file('output.pdf')

#Page upload
@app.route('/upload', methods=['GET', 'POST'])

def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload',
                                    filename=filename))
    return render_template("upload.html", uploaded_files=list_uploaded_files())

if __name__ == '__main__':
    #on ouvre une fenêtre du navigateur en écoutant le bon port
    webbrowser.open('http://127.0.0.1:5000/')
    #On lance le serveur en local
    app.run()