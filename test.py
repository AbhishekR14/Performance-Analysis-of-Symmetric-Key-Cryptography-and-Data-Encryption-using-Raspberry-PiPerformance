from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash,
    request
)
import os
import upload
from logincheck import logincheck
from downloadfile import*
from Aesdecrypt import *
import AesEncrypt
from AesEncrypt import *
from werkzeug.utils import secure_filename
from flask import send_from_directory
import docx2txt

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt','docx','pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pics= os.path.join('static','pics')
app.config['UPLOAD_FOLDER']= pics

@app.route('/')
def start():
    return redirect(url_for('login'))

import os 
from flask import send_from_directory     


@app.route('/profile', methods=['GET', 'POST'])    
def profile(): 
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error =''
    pic1=os.path.join(app.config['UPLOAD_FOLDER'],'loginpic.jpg')
    if request.method == 'POST':
        
        global emailv
        emailv=request.form.get("username")
        passwordv=request.form.get("password")
        check=logincheck(emailv,passwordv)
        if check == "Access granted":
            return redirect(url_for('profile'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', loginimg=pic1, error=error)

@app.route('/download', methods=['GET', 'POST'])
def download():
    data=''
    if request.method == 'POST':
        global fname,fid,fkey
        fname=request.form.get("fname")             
        fid=request.form.get("fid")                
        fkey=request.form.get("fkey")
        down(fname,fid)
        if checkfile(fname) == 1:
            return render_template('downloadoptions.html',output=data) 
        else:
            data=data+"Try Again"
            return render_template('filenotfound.html',output=data)
    return render_template('downloadfile.html')

@app.route('/viewdownload', methods=['GET', 'POST'])
def viewdownload():
    data=''
    data=data+decrypt(fname,fkey)
    newfile(data,fname)
    return render_template('filedownloaded.html',output=data) 

@app.route('/viewdownloaddox', methods=['GET', 'POST'])
def viewdownloaddox():
    data=''
    data=data+decrypt(fname,fkey)
    newfiledox(data,fname)
    return render_template('filedownloaded.html',output=data)

@app.route('/printdownload', methods=['GET', 'POST'])
def printdownload():
    
    return render_template('printdownload.html')



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/printfile', methods=['GET', 'POST'])
def printfile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload_file'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload_file'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            L=filename.split('.')
            filename = L[0]+ '.txt'
            if L[1]== 'docx':
                print(L[1])
                data = docx2txt.process(file)

            elif L[1] == 'txt':
                print(L[1])
                file.stream.seek(0) # seek to the beginning of file
                data = file.read()
            
            
            return render_template('printdownload.html')
    return render_template('uploadfile.html')
    
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload_file'))
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('upload_file'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            L=filename.split('.')
            filename = L[0]+ '.txt'
            if L[1]== 'docx':
                print(L[1])
                data = docx2txt.process(file)
                data = data.encode()

            elif L[1] == 'txt':
                print(L[1])
                file.stream.seek(0) # seek to the beginning of file
                data = file.read()

            key = AesEncrypt.AESmain(data, filename)
            upload.Upload_file(key,emailv,filename)
            
            return render_template('fileuploaded.html')
    return render_template('uploadfile.html')

app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
        
if (__name__ == '__main__'):
    app.run(debug=True)
