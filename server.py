    # -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/marcelo/Documents/Insper/Tecnologicas Web/AttendenceListFlask/static/photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
        return str(str(tecweb.id) + "," + str(camfis.id) + "," + str(eletromag.id) + "," +  str(modcom.id) + "," + str(empred.id))
    else:
        return ""


def transformIdToName(id):
    if id == 34:
        return "Engenharia da Computacao, 4 Semestre"


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
    semesterName = db.Column(db.String(120), unique=False)
    photoUrl = db.Column(db.String(120), unique=True)

    def __init__(self, name, email,password, isProfessor, semesterName, photoUrl):
        self.name = name
        self.email = email
        self.password = password
        self.isProfessor = isProfessor
        self.semesterName = semesterName
        self.photoUrl = photoUrl


@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'POST':

        #FINAL DO CADASTRO ALUNO
        if request.form["btn"] == "concluir":
            print("Concluir")
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            course = request.form["curso"]
            semester = request.form["semestre"]
            classId = int(course + semester)
            isProfessor = False
            semesterName = transformIdToName(classId)
            # check if the post request has the file part
            if 'file' not in request.files:
                print("NOFILE")
                return render_template('login.html')
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                print("NOFILENAME")
                return render_template('login.html')
            if file and allowed_file(file.filename):
                filename = email
                print(file.content_type)
                photoUrl = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], email))
            user = User(name = name, email= email, password= password, isProfessor = isProfessor, semesterName = semesterName, photoUrl = photoUrl)
            user.classId = convertClassId(classId)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')

        #FINAL DO CADASTRO PROFESSOR
        elif request.form["btn"] == "concluir2":
            print("Concluir")
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            listClass = request.form.getlist("class_prof")
            listClass = [str(y) for y in listClass]
            stringClass = ','.join(map(str, listClass))
            isProfessor = True
            # check if the post request has the file part
            if 'file' not in request.files:
                print("NOFILE")
                return render_template('login.html')
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                print("NOFILENAME")
                return render_template('login.html')
            if file and allowed_file(file.filename):
                filename = email
                print(file.content_type)
                photoUrl = filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], email))
            user = User(name = name, email= email, password= password, isProfessor = isProfessor, semesterName = "Professor", photoUrl = photoUrl)
            user.classId = stringClass
            db.session.add(user)
            db.session.commit()
            return render_template('login.html')

        #TENTATIVA DE LOGIN
        elif request.form["btn"] == "login":
            print("Login")
            login = request.form["email_login"]
            password = request.form["password_login"]
            try:
                user = User.query.filter_by(email=login).first()
                if user.password == password:
                    if not user.isProfessor:

                        #O QUE ACONTECE DEPOIS DO LOGIN PARA ALUNO
                        idAulas = user.classId.strip().split(",")
                        Aulas = []
                        for i in idAulas:
                            aula = Aula.query.filter_by(id = i).first()
                            Aulas.append(aula)
                        return render_template('aluno.html', aulas = Aulas, user = user)
                    elif user.isProfessor:

                        #O QUE ACONTECE DEPOIS DO LOGIN PARA Professor
                        idAulas = user.classId.strip().split(",")
                        Aulas = []
                        for i in idAulas:
                            Aulas.append(i)
                        return render_template('professor_inicial.html', aulas = Aulas, user = user)
                else:
                    print("ERRO PASSWORD")
                    #CASO LOGIN DE ERRADO
                    return "Usuário não encontrado",404
            except:
                print("ERRO TRY EXCEPT")
                return "Usuário não encontrado",404
        else:
            return render_template('login.html')
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
