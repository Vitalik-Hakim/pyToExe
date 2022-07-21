# importing the required libraries
import os
from flask import Flask, render_template, request, send_file, flash
from scipy import rand
from werkzeug.utils import secure_filename
import datetime
import hashids
import random




## Implementing Ticket naming system
hashids = hashids.Hashids(salt="this is my exe and salt", )


# initialising the flask app
app = Flask(__name__)

app_data = {
    "name":         "Python to  EXE CONVERTER",
    "description":  "A web application to convert python .py files to .exe",
    "author":       "Vitalik Hakim",
    "html_title":   "Python to EXE CONVERTER",
    "project_name": "PYTHON TO EXE WEBAPP",
    "keywords":     "PYTHON, .PY, exe, convert"
}


# Creating the upload folder
upload_folder = "uploads"
if not os.path.exists(upload_folder):
   os.mkdir(upload_folder)

# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = upload_folder

# configuring the allowed extensions
allowed_extensions = ['py',]

def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions

# The path for uploading the file
@app.route('/')
def index():
   return render_template('index.html', app_data=app_data)

@app.route('/upload-page')
def uploadpage():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
   if request.method == 'POST': # check if the method is post
      files = request.files.getlist('files') # get the file from the files object
      print(files)
      basename = "my_exe_ticket"
      randInt = random.randint(0,5000)
      rands = hashids.encode(randInt)
      suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
      filenamed = "_".join([basename,rands,suffix]) # e.g. 'my_exe_ticket_XDJSs3N_120508_171442'
      for f in files:
         print(f.filename)
         print(filenamed)
         # Saving the file in the required destination
         if check_file_extension(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(filenamed+".py"))) # this will secure the file
            res = os.listdir('uploads')
            print(res)
            position = res.index(filenamed+'.py')
            # each File takes about one minute to process so
            time = 60*position+1 # for 0 indexing of lists/ possible for first person
            if time == 1:
                time = 60
            
      return render_template('return.html',app_data=app_data,filenamed=filenamed,time=time)


# Download


@app.route('/download-page')
def downloadPage():
   return render_template('download.html')

# Sending the file to the user
@app.route('/download')
def download():

   return send_file('server-web.py', as_attachment=True)

@app.route('/ticket', methods =["GET", "POST"])
def ticket():
    if request.method == "POST":
       # getting input with ticket in HTML form
       ticket_id = request.form.get("download-ticket")
       res = os.listdir('downloads')
       print(res)
       if ticket_id+".exe" in res:

            return send_file('downloads//{}.exe'.format(ticket_id), as_attachment=True)
            
            
       else:
        flash('Ticket not found')
    return render_template('ticket.html',app_data=app_data)
@app.route('/service')
def service():
    return render_template('service.html', app_data=app_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', app_data=app_data)

@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)

if __name__ == '__main__':
    app.secret_key = 'xxxxxxxx'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run() # running the flask app
