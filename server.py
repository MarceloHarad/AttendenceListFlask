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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convertClassId(id):
    #Converte o ID do Semestre e Curso para uma lista de classes
    if id == 34:
        tecweb = Aula("Tecnologias Web", 10)
        db.session.add(tecweb)
        camfis = Aula("Camada Fisica da Computacao", 10)
        db.session.add(camfis)
        eletromag = Aula("Eletromagnetismo", 10)
        db.session.add(eletromag)
        modcom = Aula("Modelagem e Controle", 10)
        db.session.add(modcom)
        empred = Aula("Empreendedorismo Tecnologico", 10)
        db.session.add(empred)
        db.session.commit()
        return str(tecweb.id) + str(camfis.id) + str(eletromag.id) + str(modcom.id) + str(empred.id)
    else:
        return ""

class Aula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=False)
    numAulas = db.Column(db.Integer(), unique=False)
    numFaltas = db.Column(db.Integer(), unique=False)
    isActive = db.Column(db.Boolean(), unique=False)

    def __init__(self,nome,numAulas):
        self.nome = nome
        self.numAulas = numAulas
        self.numFaltas = 0
        self.isActive = False


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), unique=False)
    isProfessor = db.Column(db.Boolean(), unique=False)
    classId = db.Column(db.String(120), unique=False)
    #photoUrl = db.Column(db.String(120)), unique=True)

    def __init__(self, name, email,password, isProfessor):
        self.name = name
        self.email = email
        self.password = password
        self.isProfessor = isProfessor


@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        #FINAL DO CADASTRO
        if request.form["btn"] == "concluir":
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            course = request.form["curso"]
            semester = request.form["semestre"]
            classId = int(course + semester)
            isProfessor = False
            user = User(name = name, email= email, password= password, isProfessor = isProfessor)
            user.classId = convertClassId(classId)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')
        #TENTATIVA DE LOGIN
        elif request.form["btn"] == "login":
            login = request.form["email_login"]
            password = request.form["password_login"]
            user = User.query.filter_by(email=login).first()
            if user.password == password:
                #O QUE ACONTECE DEPOIS DO LOGIN
                return user.name + " e-mail: &lt;" + user.email + "&gt;"
            else:
                #CASO LOGIN DE ERRADO
                return "Usuário não encontrado",404
    else:
        return render_template('login.html')

@app.route('/read/<email>')
def read_user(email):
	user = User.query.filter_by(email=email).first()
	if(user):
    	  return user.name + " e-mail: &lt;" + user.email + "&gt;"
	else:
    	  return "Usuário não encontrado",404

db.create_all()

if __name__ == "__main__":
    app.run()
