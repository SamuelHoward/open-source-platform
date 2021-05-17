from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('projects.html', projects=Projects.query.all())
