    # -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/marcelo/Documents/Insper/Tecnologicas Web/AttendenceListFlask/photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 's3cr3t'
db = SQLAlchemy(app)


class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=False)
    numAulas = db.Column(db.Integer(), unique=False)
    numFaltas = db.Column(db.Integer(), unique=False)

    def __init__(self,nome,numAulas):
        self.nome = nome
        self.numAulas = numAulas
        self.numFaltas = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)
    classId = db.Column(db.Integer(), unique=False)
    #photoUrl = db.Column(db.String(120)), unique=True)

    def __init__(self, username, email,password, classId):
        self.username = username
        self.email = email
        self.password = password
        self.classId

    def chooseClass(self,nome,numAulas):
        aula = Aula(nome,numAulas)
        self.classId = aula.id
        db.session.add(aula)
        db.session.commit()


@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        course = request.form["curso"]
        semester = request.form["semestre"]
        classId = int(course + semester)
        isProfessor = False
        print("KKK")
    else:
        return render_template('login.html')

    '''
    print("OK")
    nome = request.form["name"]
    email = request.form["email"]
    #password = request.form["password"]
    curso = request.form["curso"]
    semestre = request.form["semetre"]
    classId = int(curso + semestre)
    user = User(username=username, email=email, classId=classId)
    db.session.add(user)
    db.session.commit()
    '''


if __name__ == "__main__":
    app.run()
