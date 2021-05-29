from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    return render_template('projects.html', projects=Projects.query.paginate(page=page, per_page=50))

@app.route('/organizations')
def organizations():
    page = request.args.get('page', 1, type=int)
    return render_template('organizations.html', organizations=Organizations.query.paginate(page=page, per_page=50), projects=Projects.query.all())

search_results_data = Projects.query.filter(Projects.description.contains(""))
search_term = None

@app.route('/projects_search', methods=['GET', 'POST'])
def projects_search():
    global search_results_data
    global search_term
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        search_term=request.form['search_term']
        search_results_data = Projects.query.filter(Projects.description.contains(search_term))
        return redirect(request.path)
    else:
        return render_template('projects_search.html', search_results=search_results_data.paginate(page=page, per_page=50), search_term=search_term)
