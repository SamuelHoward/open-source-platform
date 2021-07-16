# Import necessary modules
from flask import Blueprint, render_template, request, redirect, url_for, \
    request, flash
from flask_app import db, app
from flask_app.models import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

# This files includes all the routes for authentication
auth = Blueprint('auth', __name__)

# Set up mail instance
app.config.update(
    MAIL_USERNAME = 'theopensourceplatform@gmail.com',
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD'],
    MAIL_PORT=465,
    MAIL_USE_SSL = True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_DEFAULT_SENDER= \
    '"TheOpenSourcePlatform" <theopensourceplatform@gmail.com>')

mail = Mail(app)

# Route for logging in
@auth.route('/login', methods=['GET', 'POST'])
def login():

    # Logic for logging in
    if request.method == 'POST':

        # Get the data from the form
        email = request.form.get('email')
        password = request.form.get('password')

        # Get the data for the potential logged in user
        name_q = db.session.query(Users.name).filter(Users.email==email)
        id_q = db.session.query(Users.id).filter(Users.email==email)
        pass_q = db.session.query(Users.password).filter(Users.email==email)

        # If the user exists, continue authenticating
        if db.session.query(id_q.exists()).scalar():

            # If the password is incorrect, authentication fails
            if not check_password_hash(pass_q.first()[0], password):

                # Inform the user that their login has failed
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login'))

            # Find the correctly authenticated user
            user = Users(id=id_q.first()[0],
                         email=email,
                         name=name_q.first()[0],
                         password=pass_q.first()[0])

            # Login the user
            login_user(user)
            
            # Flash login message
            flash('Successfully logged in')
            
            # Load the user's profile page
            return redirect(url_for('main.profile'))

        # if the user does not exist, do not log in
        else:

            # Inform the user that the entered email is incorrect
            flash('The email you entered is not associated with an account.')
            return redirect(url_for('auth.login'))
        
    # Render the login page
    else:
        return render_template('login.html', title='OSP | Login')

# Route for signing up
@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    # Logic for signing up a user
    if request.method == 'POST':

        # Get the data from the form
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if the user's email already belongs to an account
        q = db.session.query(Users.id).filter(Users.email==email)

        # If the user's email exists, signup fails
        if db.session.query(q.exists()).scalar():
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # Create the Users record
        new_user = Users(
            id=random.randint(-2147483648, 2147483647),
            email=email,
            name=name,
            password=generate_password_hash(password, method='sha256'))

        # Add the user and commit
        db.session.add(new_user)
        db.session.commit()

        # Craft the confirmation email and send it
        msg = Message("Open Source Platform | Signup Confirmation",
                      recipients=[email])
        mail.send(msg)
        
        # Login the new user
        login_user(new_user)

        # flash sign up message
        flash('Successfully signed in')
        
        # Load the login page
        return redirect(url_for('main.profile'))

    # Render the signup page
    else:
        return render_template('signup.html', title='OSP | Sign up')

# Route for logging out
@auth.route('/logout')
@login_required
def logout():

    # Log out the user and return to homepage
    logout_user()

    # Flash log out message
    flash('Successfully logged out')
    
    return redirect(url_for('index'))
