from flask import make_response

from app import app
from flask import render_template, redirect, request,abort
from app.models.job import Job
from app.models.send_grid import SendGridEmail
from  app.models.page import Pagination


@app.route("/")
def index():
    num = 0
    db = Job()
    jobs = db.list_jobs(int(0))
    return render_template('default/list_job.html', jobs= jobs, numero= num ,pagination= 0)


@app.route("/contato")
def contato():
    """
    Metodo que rendeliza o html, ele depende do send_contato()
    :return:
    """
    return render_template("default/contato.html")


@app.route("/sobre")
def sobre():
    """
    Metodo que mostra o html sobre
    :return:
    """
    return render_template("default/sobre.html")


@app.route("/search", methods=['POST'])
def search():
    """
    MEtodo responsavel pela busca de vagas
    :return:
    """
    word_pass = request.form['pass_key']
    db = Job()
    jobs = db.search_jobs(word_pass)
    return render_template("default/busca.html", jobs=jobs)

@app.route("/job/<id>")
def job(id):
    db = Job()
    resultado = db.find_id(id)
    return render_template("default/job.html",resultado=resultado)

@app.route('/logout')
def delete_token():
    """
    Função sair  da aplicação
    :return:
    """
    resp = make_response(redirect("/"))
    resp.set_cookie('token', '', expires=0)
    return resp


@app.route("/send_contato", methods=['POST', 'GET'])
def send_contato():
    """
    Metodo usado para o envio de email para o adm.
    :return:
    """
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['msg']
        envio = SendGridEmail()
        envio.send_me(name, email, message)
        return redirect('/')
    except Exception as e:
        return e

@app.route("/politica")
def politica():
    return render_template("default/politica.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('default/404.html'), 404


@app.route('/page/<int:num>')
def page(num):
    num = int(num)
    db = Job()
    jobs = db.list_jobs(num)
    pagination = (db.count_jobs() / 10)
    if num > pagination:
        return redirect('/')
    else:
        return render_template('default/list_job.html', jobs= jobs,numero=num,pagination=round(pagination))