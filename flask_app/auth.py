from flask import Blueprint
from flask_app import db
from flask_login import login_user
from flask_app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required
import random

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        name_q = db.session.query(Users.name).filter(Users.email==email)
        id_q = db.session.query(Users.id).filter(Users.email==email)
        pass_q = db.session.query(Users.password).filter(Users.email==email)
        
        if db.session.query(id_q.exists()).scalar():
            if not check_password_hash(pass_q.first()[0], password):
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login'))

        user = Users(id=id_q.first()[0], email=email, name=name_q.first()[0], password=pass_q.first()[0])
        print(user)
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    else:
        return render_template('login.html', title='OSP | Login')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        q = db.session.query(Users.id).filter(Users.email==email)
        if db.session.query(q.exists()).scalar():
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = Users(id=random.randint(-9223372036854775808, 9223372036854775807), email=email, name=name, password=generate_password_hash(password, method='sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', title='OSP | Sign up')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
