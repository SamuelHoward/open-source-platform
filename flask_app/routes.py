from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *
from sqlalchemy import or_

'''
@app.route('/')
@app.route('/index')
@app.route('/projects')
def index():
    page = request.args.get('page', 1, type=int)
    return render_template('projects.html', projects=Projects.query.paginate(page=page, per_page=50))
'''

orgs_search_results_data = Organizations.query.filter(Organizations.name.contains(""))
projects_search_results_data = Projects.query.filter(Projects.description.contains(""))
search_term = None

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    global projects_search_results_data
    global search_term
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_term=request.form['search_term']
        projects_search_results_data = Projects.query.filter(
            or_(Projects.description.contains(search_term),
                Projects.name.contains(search_term),
                Projects.language.contains(search_term),
                Projects.owner.contains(search_term),
                Projects.source.contains(search_term)))
        if 'name' in request.form:
            projects_search_results_data = projects_search_results_data.order_by(Projects.name)
        return redirect(request.path)
    else:
        return render_template('projects_search.html', search_results=projects_search_results_data.paginate(page=page, per_page=50), search_term=search_term)

@app.route('/organizations', methods=['GET', 'POST'])
def organizations():
    global orgs_search_results_data
    global search_term
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_term=request.form['search_term']
        orgs_search_results_data = Organizations.query.filter(Organizations.name.contains(search_term))
        if 'name' in request.form:
            orgs_search_results_data = orgs_search_results_data.order_by(Organizations.name)
        return redirect(request.path)
    else:
        return render_template('organizations.html', search_results=orgs_search_results_data.paginate(page=page, per_page=50), search_term=search_term, projects=Projects.query.all())


'''
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/projects', methods=['GET', 'POST'])
def projects_search():
    global search_results_data
    global search_term
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_term=request.form['search_term']
        search_results_data = Projects.query.filter(
            or_(Projects.description.contains(search_term),
                Projects.name.contains(search_term),
                Projects.language.contains(search_term),
                Projects.owner.contains(search_term),
                Projects.source.contains(search_term)))
        return redirect(request.path)
    else:
        return render_template('projects.html', search_results=search_results_data.paginate(page=page, per_page=50), search_term=search_term)
'''
