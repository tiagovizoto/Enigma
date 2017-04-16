from app import app
from app.models.job import Job
from app.models.rh import Rh
from app.models.token import Token
from app.models.send_grid import SendGridEmail
from flask import render_template,redirect,request, make_response,jsonify, Response
from datetime import datetime, timedelta
from time import gmtime, strftime, mktime
import random, os, json
from datetime import datetime, timedelta
from bson.json_util import dumps


@app.route("/rh/login")
def login_token():
    if request.cookies.get("token"):
       return redirect("/rh/" + request.cookies.get("token"))
    return render_template("rh/token.html")


@app.route("/rh/", methods=['POST','GET'])
def manager():
    """
    Metodo de escape. Caso o tenha o token armazenado no cookie é redirecionado para sua pagina.
    :return:
    """
    if request.method == 'GET':
        return redirect("/rh/login")
    elif request.method == 'POST':
        if request.cookies.get("token"):
            return redirect("/rh/" + request.cookeis.get('token'))
        else:
            if request.form['token']:
                return redirect('/rh/'+request.form['token'])
            else:
                return redirect("/rh/login")

@app.route("/rh/<token>")
def manager_rh(token):
    """
    :param token:
    :return:
    """
    futuro = datetime.now()
    futuro += timedelta(days=1)
    m_j = Job()
    m_t = Token()
    if not m_t.find_token(token):
        return redirect('/')
    else:
        v = m_t.find_token(token)
        vagas = m_j.find_jobs_email(v['email'])

        resp = make_response(render_template('rh/manager_rh.html', vagas=vagas))
        if not request.cookies.get('token'):
                resp.set_cookie('token', token, expires=mktime(futuro.timetuple()), path='/')
        return resp


@app.route("/rh/job/new")
def new_job():
    """
    Metodo usado para rendelizar html
    :return:
    """
    futuro = datetime.now()
    futuro += timedelta(days=30)
    return render_template("rh/new_job.html", fim = futuro.strftime('%Y-%m-%d'))


@app.route("/rh/job/<id>/delete")
def remove_job(id):
    token = Token()
    job = Job()
    rh = Rh()
    token_text = request.cookies.get("token")

    if token_text:
        rh_result = token.find_token(token_text)
        result_job = job.find_id(id)
        if rh_result[0]['email'] == result_job['job']['business']['email']:
            rh.delete_job(id)
            return redirect("/rh/")
    return redirect("/")

@app.route("/rh/job/<id>/edit")
def edit_job(id):
    token = Token()
    v = Job()
    if request.get_cookie('token'):
        email = token.find_token(request.get_cookie('token'))
        job = v.find_id(id)

        if email[0]['email'] == job['job']['business']['email']:
            return render_template('edit', job=job)
        else:
            redirect('/rh')
    else:
        redirect('/rh')


@app.route("/rh/job/<int:id>/update")
def update_job(id):
    token = Token()
    v = Job()
    if request.get_cookie('token'):
        email = token.find_token(request.cookies.get('token'))
        job = v.find_id(id)

        if email[0]['email'] == job['business']['email']:
            title = request.form['title']
            location = request.form['location']
            business = request.form['business']
            salary = request.form['salary']
            description = request.form['description']
            email = request.form['email']
            date_valid = request.form['date_valid']
            coin = request.form['coin']
            period_pay = request.form['period_pay']
            if not request.form['linkjob']:
                 linkjob = False
            else:
                linkjob = request.forms.linkjob

            # data mongodb
            job_json = {
                'title': title,
                'location': location,
                'description': description,
                'business': {
                    'name': business,
                    'email': email,
                },
                'salary': {
                    'value': salary,
                    'coin': coin,
                    'period_pay': period_pay
                },
                'date_valid': date_valid,
                'date_post': datetime.datetime.now(),
                'link':linkjob
            }
            # add in mongo
            w = Rh()
            w.update_job(id, job_json)

        else:
            redirect('/manager')
    else:
        redirect('/manager')


@app.route("/job/add", methods=['POST'])
def add_job():

    #request for form
    title = request.form['title']
    location = request.form['location']
    business = request.form['business']
    salary = request.form['salary']
    description = request.form['description']
    email = request.form['email']
    date_valid = request.form['date_valid']
    coin = request.form['coin']
    period_pay = request.form['period_pay']
    linkjob = request.form['linkjob']
    #data mongodb
    job_json = {
                'title': title,
                'location': location,
                'description': description,
                'business': {
                    'name':business,
                    'email':email,
                },
                'salary': {
                    'value': salary,
                    'coin': coin,
                    'period_pay': period_pay
                },
                'date_valid': date_valid,
                'date_post': strftime("%Y-%m-%d", gmtime()),
                'link': linkjob,
                'candidaty':[]
                }
    #add in mongo
    w = Rh()
    print(w.new_job(job_json))
    return redirect('/')


@app.route("/rh/new/job/")
def new_job_rh():
    db = Rh()
    t = Token()
    futuro = datetime.now()
    futuro += timedelta(days=30)

    token = request.cookies.get("token")
    if request.method == 'GET':
        if token:
            email = t.find_token(token)
            if email:
                print(email["email"])
                profile = db.search_profile(email=email["email"])
                if profile:
                    return render_template("rh/new_job_rh.html", profile_my=profile, fim=futuro.strftime('%Y-%m-%d'))
    return redirect("/rh/job/new")

@app.route("/job/add2", methods=['POST'])
def add_job2():
    data = request.get_json()
    print(data)
    rh = Rh()
    _id = rh.new_job(data)
    print(_id)
    data = {
        'id': str(_id),
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://enigmajob.xyz'

    return resp


@app.route("/new_token", methods=['POST'])
def new_token():
    token = Token()
    email = request.form['email']
    SendToken = SendGridEmail()
    token_text = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQSRVTUWYZabcdefghiklmnopqzyx') for i in range(16))
    token.insert_token(token_text,email)
    SendToken.send_token(token_text,email)
    return redirect("/")


@app.route("/rh/profile/", methods=['GET','POST'])
def profile_rh():

    db = Rh()
    t = Token()
    token = request.cookies.get("token")
    if request.method == 'GET':
        if token:
            email = t.find_token(token)
            if email:
                print(email["email"])
                profile = db.search_profile(email=email["email"])
                if profile:
                    return render_template("rh/profile_rh.html", profile_my=profile)
                else:
                    return render_template("rh/profile_rh.html", profile_my=None, email=email["email"])
        else:
            return redirect("/")
    elif request.method == 'POST':
        name_business = request.form['name_business']
        location = request.form["location"]
        name_pearson = request.form["name_pearson"]
        description = request.form["description"]
        website_business = request.form["website_business"]
        email = request.form["email"]
        data_profile = {
            'name_pearson':name_pearson,
            'location':location,
            'description':description,
            'website_business':website_business,
            'name_business':name_business,
            'email':email
        }
        db.create_profile(profile=data_profile)
        return redirect('/rh/profile/')

@app.route("/rh/profile/edit/<id>", methods=['POST','GET'])
def edit_profile_rh(id):
    t = Token()
    db = Rh()
    if request.method == 'GET':
        token = request.cookies.get("token")
        if token:
            result_token = t.find_token(token)
            profile = db.search_profile(email=result_token["email"])
            if profile["email"] == result_token["email"]:
                return render_template("rh/profile_rh_edit.html", profile_my = profile)
    elif request.method == 'POST':
        name_business = request.form['name_business']
        location = request.form["location"]
        name_pearson = request.form["name_pearson"]
        description = request.form["description"]
        website_business = request.form["website_business"]
        email = request.form["email"]
        data_profile = {
            'name_pearson': name_pearson,
            'location': location,
            'description': description,
            'website_business': website_business,
            'name_business': name_business,
            'email': email
        }
        db.update_profile(id,data_profile)
        return redirect("/rh/profile/")




