    # -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import time


UPLOAD_FOLDER = '/home/marcelo/Documents/Insper/Tecnologicas Web/AttendenceListFlask/static/photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convertClassId(id, nome):
    #Converte o ID do Semestre e Curso para uma lista de classes
    if id == 31:
        desoft = Aula("Design de Software", 10, nome)
        db.session.add(desoft)
        natdes = Aula("Natureza do Design", 10, nome)
        db.session.add(natdes)
        modsim = Aula("Modelagem e Simulação do Mundo Físico", 10, nome)
        db.session.add(modsim)
        instmed = Aula("Instrumentação e Medição", 10, nome)
        db.session.add(instmed)
        gde = Aula("Grandes Desafios da Engenhariia", 10, nome)
        db.session.add(gde)
        db.session.commit()
        return str(str(desoft.id) + "," + str(natdes.id) + "," + str(modsim.id) + "," +  str(instmed.id) + "," + str(gde.id))
    elif id == 32:
        codesign = Aula("Codesign de Apps", 10, nome)
        db.session.add(codesign)
        fismov = Aula("Física do Movimento", 10, nome)
        db.session.add(fismov)
        acion = Aula("Acionamentos Elétricos", 10, nome)
        db.session.add(acion)
        cdados = Aula("Ciência dos Dados", 10, nome)
        db.session.add(cdados)
        matvar = Aula("Matemática da Variação", 10, nome)
        db.session.add(matvar)
        db.session.commit()
        return str(str(codesign.id) + "," + str(fismov.id) + "," + str(acion.id) + "," +  str(cdados.id) + "," + str(matvar.id))
    elif id == 33:
        desagil = Aula("Desenvolvimento Colaborativo Ágil", 10, nome)
        db.session.add(desagil)
        rob = Aula("Robótica Computacional", 10, nome)
        db.session.add(rob)
        elesist = Aula("Elementos do Sistema", 10, nome)
        db.session.add(elesist)
        matmult = Aula("Matemática Multivariada", 10, nome)
        db.session.add(matmult)
        descmat = Aula("Desconstruindo a Materia", 10, nome)
        db.session.add(descmat)
        db.session.commit()
        return str(str(desagil.id) + "," + str(rob.id) + "," + str(elesist.id) + "," +  str(matmult.id) + "," + str(descmat.id))
    elif id == 34:
        tecweb = Aula("Tecnologias Web", 10, nome)
        db.session.add(tecweb)
        camfis = Aula("Camada Fisica da Computacao", 10, nome)
        db.session.add(camfis)
        eletromag = Aula("Eletromagnetismo", 10, nome)
        db.session.add(eletromag)
        modcom = Aula("Modelagem e Controle", 10, nome)
        db.session.add(modcom)
        empred = Aula("Empreendedorismo Tecnologico", 10, nome)
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
    isPresent = db.Column(db.Boolean(), unique=False)
    nameStudent = db.Column(db.String(80), unique=False)

    def __init__(self,nome,numAulas,nameStudent):
        self.nome = nome
        self.numAulas = numAulas
        self.numFaltas = 0
        self.isActive = False
        self.nameStudent = nameStudent
        self.isPresent = False


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
            user.classId = convertClassId(classId, user.name)
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
            user = User.query.filter_by(email=login).first()
            if user.password == password:
                if not user.isProfessor:

                    #O QUE ACONTECE DEPOIS DO LOGIN PARA ALUNO
                    idAulas = user.classId.strip().split(",")
                    Aulas = []
                    for i in idAulas:
                        aula = Aula.query.filter_by(id = i).first()
                        Aulas.append(aula)
                    aula_ativa = False
                    for i in Aulas:
                        if i.isActive:
                            aula_ativa = True
                            nome_aula = i.nome
                    if not aula_ativa:
                        nome_aula = ""
                    return render_template('aluno.html', aulas = Aulas, user = user, aula_ativa = aula_ativa, nome_aula = nome_aula)
                else:

                    #O QUE ACONTECE DEPOIS DO LOGIN PARA Professor
                    idAulas = user.classId.strip().split(",")
                    Aulas = []
                    for i in idAulas:
                        Aulas.append(i)
                    print(Aulas)
                    return render_template('professor_inicial.html', aulas = Aulas, user = user)


            else:
                print("ERRO PASSWORD")
                #CASO SENHA DE ERRADO
                return "Usuário não encontrado",404

        elif request.form["btn"] == "open_list":
            print("open_list")
            classe = request.form["aulas"]
            list_classes = Aula.query.filter_by(nome=classe).all()
            for i in list_classes:
                i.isActive = True
            db.session.commit()
            return render_template('login.html')

        elif request.form["btn"] == "close_list":
            print("close_list")
            classe = request.form["aulas"]
            list_classes = Aula.query.filter_by(nome=classe).all()
            for i in list_classes:
                i.isActive = False
                if i.isPresent == False:
                    i.numFaltas += 1
                i.isPresent = False
            db.session.commit()
            return render_template('login.html')

        elif request.form["btn"] == "sign":
            print("sign")
            id_aula = request.form["aulas_aluno"]
            aula = Aula.query.filter_by(id=int(id_aula)).first()
            aula.isPresent = True
            print(aula.nome)
            db.session.commit()
            return render_template('login.html')

        elif request.form["btn"] != None:
            ("NONE")
            classe = request.form["btn"]
            list_classes = Aula.query.filter_by(nome=classe).all()
            email = request.form["email_professor"]
            user = User.query.filter_by(email=email).first()
            date = time.strftime('%d/%m/%Y')
            return render_template('professor.html', aulas = list_classes, user = user, date = date, nome_aula = classe)

        else:
            print("else")
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
