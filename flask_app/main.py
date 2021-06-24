from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *
from sqlalchemy import or_, and_, func
from flask import Blueprint
from flask_login import login_required, current_user
import random

main = Blueprint('main', __name__)

orgs_search_results_data = Organizations.query.filter(Organizations.name.contains(""))
projects_search_results_data = Projects.query.filter(Projects.description.contains(""))
search_term = None
projectsPerPage = 25
orgsPerPage = 25

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Open Source Platform')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    global projects_search_results_data
    global search_term
    global projectsPerPage
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST' and 'search_term' in request.form:
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
        elif 'sort_by' in request.form and request.form['sort_by'] == 'forks':
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data.order_by(Projects.forks)
            else:
                projects_search_results_data = projects_search_results_data.order_by(Projects.forks.desc())
        elif 'sort_by' in request.form and request.form['sort_by'] == 'watchers':
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data.order_by(Projects.watchers)
            else:
                projects_search_results_data = projects_search_results_data.order_by(Projects.watchers.desc())
        elif 'sort_by' in request.form and request.form['sort_by'] == 'issues':
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data.order_by(Projects.open_issues)
            else:
                projects_search_results_data = projects_search_results_data.order_by(Projects.open_issues.desc())
        return redirect(request.path)
    elif request.method == 'POST' and 'fav_name' in request.form:
        favorite=Favorites.query.filter(and_(Favorites.user_id==current_user.id, Favorites.fav_name==request.form['fav_name'])).first()
        if favorite is None:
            new_fav = Favorites(id=random.randint(-9223372036854775808, 9223372036854775807), user_id=current_user.id, fav_name=request.form['fav_name'], fav_type='project')
            db.session.add(new_fav)
            db.session.commit()
        return redirect(request.path)
    elif request.method == 'POST' and 'unfav_name' in request.form:
        fav = db.session.query(Favorites).filter(and_(Favorites.user_id==current_user.id, Favorites.fav_name==request.form['unfav_name'])).first()
        db.session.delete(fav)
        db.session.commit()
        return redirect(request.path)
    else:
        return render_template('projects_search.html', search_results=projects_search_results_data.paginate(page=page, per_page=projectsPerPage), search_term=search_term, title='OSP | Projects', favorites=Favorites.query.filter(Favorites.user_id==current_user.id).with_entities(Favorites.fav_name))

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
        return render_template('organizations.html', search_results=orgs_search_results_data.paginate(page=page, per_page=orgsPerPage), search_term=search_term, projects=Projects.query.all(), title='OSP | Organizations')

@app.route('/project/<projectName>')
def project(projectName):
    try:
        proj = Projects.query.filter(Projects.name==projectName).one()
        orgName = Organizations.query.filter(Organizations.name==proj.owner).one()
        projs = Projects.query.filter(Projects.owner==orgName.name)
        count = projs.count()
        return render_template('project.html', project=proj, projects=projs, count=count, title='OSP | ' + projectName)
    except:
        return render_template('404.html', title='OSP | 404'), 404

@app.route('/org/<orgName>')
def organization(orgName):
    try:
        org = Organizations.query.filter(Organizations.name==orgName).one()
        projs = Projects.query.filter(Projects.owner==orgName)
        return render_template('organization.html', organization=org, projects=projs, title='OSP | ' + orgName)
    except:
        return render_template('404.html', title='OSP | 404'), 404

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, title='OSP | Profile', favorites=Favorites.query.filter(Favorites.user_id==current_user.id))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='OSP | 404'), 404
