#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
from flask import Flask, render_template, request, url_for, flash, redirect, send_from_directory , send_file
import os
import requests
import glob
import shutil
from pathlib import Path
from waitress import serve

DEVELOPMENT_ENV  = True

app = Flask(__name__)

app_data = {
    "name":         "Python to  EXE CONVERTER",
    "description":  "A web application to convert python .py files to .exe",
    "author":       "Vitalik Hakim",
    "html_title":   "Python to EXE CONVERTER",
    "project_name": "PYTHON TO EXE WEBAPP",
    "keywords":     "PYTHON, .PY, exe, convert"
}
DOWNLOAD_FOLDER = 'dist'
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'py', 'pyi', 'pyc', 'pyd', 'pyo', 'pyw', 'pyz'}
@app.route('/')
def index():
    return render_template('index.html', app_data=app_data)

@app.route("/upload-pyfile", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['pyfile']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file
      return redirect(url_for('convertedfile'))

@app.route('/download')
def downloadFile():
    res = os.listdir(DOWNLOAD_FOLDER)
    if len(res) == 0:
            return render_template('404.html', app_data=app_data)
    file = "".join(res)
    path = "{}\\{}".format(DOWNLOAD_FOLDER,file)
    print(path)
    
    # shutil.rmtree(DOWNLOAD_FOLDER)
    # os.mkdir(DOWNLOAD_FOLDER)
    
    return send_file(path, as_attachment=True)


@app.route('/loader')
def loader():
    return render_template('loader.html', app_data=app_data)
    

@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)

@app.route('/convertedfile')
def convertedfile():
    res = os.listdir(UPLOAD_FOLDER)
    print(res)
    filename = "".join(res)
    createDirectory = "pyinstaller --onefile {}/{}".format(UPLOAD_FOLDER,filename)
    subprocess.call(createDirectory, shell=True)
    # subprocess.Popen(['./convert.sh'],
    #              stdout=subprocess.PIPE, 
    #              stderr=subprocess.PIPE, an attempt at asynchronous running of sh script to convert py file
    #              shell=True)
    shutil.rmtree(UPLOAD_FOLDER)
    shutil.rmtree('build')
    os.mkdir(UPLOAD_FOLDER)


    return render_template('convertedfile.html', app_data=app_data)
    

@app.route('/service')
def service():
    return render_template('service.html', app_data=app_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', app_data=app_data)


# if __name__ == '__main__':
#     serve(app, port=8080, host="0.0.0.0")
    # app.run(debug=DEVELOPMENT_ENV,threaded=True)