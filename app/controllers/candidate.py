from app import app
from app.models.job import Job
from app.models.curriculum import Curriculum
from app.models.token import Token
from app.models.send_grid import SendGridEmail
from flask import render_template,redirect,request, make_response,jsonify, Response
from datetime import datetime, timedelta
from time import gmtime, strftime, mktime
import os, json
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS


@app.route("/candidate/send_curriculum")
def email():
    apply = request.forms.id_job
    id = {'apply': apply}
    print(apply)
    return render_template('sendMail', id_job=id)


@app.route('/upload', methods=['POST'])
def send_mail():
    #request of form
    id_job = request.form['id_job']
    nome = request.form['name']
    email = request.form['email']
    message = request.form['msg']
    title = request.form['title_job']
    file = request.files['file']

    #Armazenar o caminho do pdf
    save_path = os.getcwd().format(category=email)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(save_path, filename))
        envio = SendGridEmail()
        job = Job()
        toPeopleEmail = job.find_email_bussniss(id_job)
        envio.send_rh(nome, email, message, os.path.join(save_path, filename), toPeopleEmail, id_job, title)
        os.remove(os.path.join(save_path, filename))
        print(str(job.insert_pearson(id_job, nome, email)))
        return make_response(redirect('/'))
    else:
        return make_response(render_template("default/404.html"))



    #remover o pdf

    return redirect('/')


@app.route("/candidate/sing_in")
def cadastro():
    return render_template("candidate/form_curricullum.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/adicionar_curriculum", methods=['POST','GET'])
def adicionar_curriculum():
    data = request.get_json()
    curriculum = Curriculum()
    curriculum.add_curriculum(data)

    data = {
        'hello': 'true',

    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://luisrei.com'

    return resp


@app.route("/asdsadsa")
def a():
    return render_template("default/teste.html")
