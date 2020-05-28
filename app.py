#!/usr/bin/env python3

from flask import Flask, render_template, send_file, flash,request, redirect, url_for
from werkzeug.utils import secure_filename

import os
from pdfrw import PdfReader, PdfWriter

UPLOAD_FOLDER='/home/nicolas/boulot/pdf_merger/uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'jpg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])

def home():    
    return render_template("home.html")

@app.route('/fusion', methods=['GET'])

def merge():
    writer = PdfWriter()
    files = [x for x in os.listdir('uploads') if x.endswith('.pdf')]
    for fname in sorted(files):
        writer.addpages(PdfReader(os.path.join('uploads', fname)).pages)
    writer.write("output.pdf")
    return render_template("fusion.html")

@app.route('/download', methods=['GET'])

def download():
    return send_file('output.pdf')

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
    return '''
        <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
      <a href=fusion> Merge ! </a>
    </form>
    '''

if __name__ == '__main__':
    app.run()