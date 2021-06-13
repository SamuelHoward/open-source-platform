from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *
from sqlalchemy import or_, func

orgs_search_results_data = Organizations.query.filter(Organizations.name.contains(""))
projects_search_results_data = Projects.query.filter(Projects.description.contains(""))
search_term = None
projectsPerPage = 25
orgsPerPage = 25

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    global projects_search_results_data
    global search_term
    global projectsPerPage
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_term=request.form['search_term']
        projects_search_results_data = Projects.query.filter(
            or_(Projects.description.contains(search_term),
                Projects.name.contains(search_term),
                Projects.language.contains(search_term),
                Projects.owner.contains(search_term),
                Projects.source.contains(search_term)))
        if 'per_page' in request.form:
            projectsPerPage = int(request.form['per_page'])
        if 'sort_by' in request.form and request.form['sort_by'] == 'name':
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data.order_by(Projects.name.desc())
            else:
                projects_search_results_data = projects_search_results_data.order_by(Projects.name)
        elif 'sort_by' in request.form and request.form['sort_by'] == 'created':
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data.order_by(func.date(Projects.created_time))
            else:
                projects_search_results_data = projects_search_results_data.order_by(func.date(Projects.created_time).desc())
        return redirect(request.path)
    else:
        return render_template('projects_search.html', search_results=projects_search_results_data.paginate(page=page, per_page=projectsPerPage), search_term=search_term)

@app.route('/organizations', methods=['GET', 'POST'])
def organizations():
    global orgs_search_results_data
    global search_term
    global orgsPerPage
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_term=request.form['search_term']
        orgs_search_results_data = Organizations.query.filter(Organizations.name.contains(search_term))
        if 'per_page' in request.form:
                        orgsPerPage = int(request.form['per_page'])
        if 'name' in request.form:
            if 'reverse' in request.form:
                orgs_search_results_data = orgs_search_results_data.order_by(Organizations.name.desc())
            else:
                orgs_search_results_data = orgs_search_results_data.order_by(Organizations.name)
        return redirect(request.path)
    else:
        return render_template('organizations.html', search_results=orgs_search_results_data.paginate(page=page, per_page=orgsPerPage), search_term=search_term, projects=Projects.query.all())

@app.route('/project/<projectName>')
def project(projectName):
    try:
        proj = Projects.query.filter(Projects.name==projectName).one()
        return render_template('project.html', project=proj)
    except:
        return render_template('404.html'), 404

@app.route('/org/<orgName>')
def organization(orgName):
    try:
        org = Organizations.query.filter(Organizations.name==orgName).one()
        return render_template('organization.html', organization=org, projects=Projects.query.all())
    except:
        return render_template('404.html'), 404
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
