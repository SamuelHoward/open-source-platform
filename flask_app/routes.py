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
