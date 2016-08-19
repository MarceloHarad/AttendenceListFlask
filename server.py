# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/marcelo/Documents/Insper/Tecnologicas Web/AttendenceListFlask/photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def root():
    return render_template('login.html')

if __name__ == "__main__":
    app.run()
