# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates/')
app.config['UPLOAD_FOLDER'] = 'uploaded/'
with open('secret_key.txt', 'r') as keyfile:
    app.secret_key = keyfile.read()

def full_path(filename):
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def secure_file_save(file):
    filename, file_ext = os.path.splitext(file.filename)
    full_filename = '%s%s' % (filename, file_ext)
    uniq = 1
    while os.path.exists(full_path(full_filename)):
        full_filename = '%s__(%d)%s' % (filename, uniq, file_ext)
        uniq += 1

    file.save(full_path(full_filename))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file[]' not in request.files:
            flash('ERROR: No file part')
            return redirect(request.url)
        files = request.files.getlist('file[]')
        # if user does not select file, browser also
        # submit a empty part without filename
        filenames = []
        for file in files:
            if file.filename == '':
                flash('ERROR: No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                secure_file_save(file)
                filenames.append(filename)
        flash(filenames)
        return redirect(request.url+'success')
    return render_template('index.html')

@app.route('/success', methods=['GET'])
def upload_file_check():
    return render_template('success.html')
