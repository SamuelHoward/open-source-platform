# Import necessary modules
from flask import Blueprint, render_template, request, redirect, url_for, \
    request, flash
from flask_app import db, app
from flask_app.token import generate_confirmation_token, confirm_token
from flask_app.models import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message, Mail
from flask_app.decorators import check_confirmed, check_reset
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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
            
            # If 'next' is present in url, go to that url
            if 'next' in request.args:
                return redirect(request.args.get('next'))
            
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
            password=generate_password_hash(password, method='sha256'),
            created_on=datetime.now(),
            confirmed=False)

        # Generate the user's token and create the email content
        token = generate_confirmation_token(email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        
        # Add the user and commit
        db.session.add(new_user)
        db.session.commit()

        # Craft the confirmation email and send it
        msg = Message("Open Source Platform | Signup Confirmation",
                      recipients=[email],
                      html=html)
        mail.send(msg)
        
        # Login the new user
        login_user(new_user)

        # flash sign up message
        flash('Successfully signed in')
        
        # Load the login page
        return redirect(url_for('auth.unconfirmed'))

    # Render the signup page
    else:
        return render_template('signup.html', title='OSP | Sign up')

# Route for sending a password reset email
@auth.route('/password-reset-email', methods=['GET', 'POST'])
def password_reset_email():

    # Logic for signing up a user
    if request.method == 'POST':

        # Get the data from the form
        email = request.form.get('email')

        # Check if the user's email already belongs to an account
        q = db.session.query(Users.id).filter(Users.email==email)

        # If the user's email exists, password reset fails
        if not db.session.query(q.exists()).scalar():
            flash('Email address does not exist')
            return redirect(url_for('auth.signup'))

        # Generate a new token using the user's email
        token = generate_confirmation_token(email)

        # Generate the email message and send it
        confirm_url = url_for('auth.forgot_password', token=token, _external=True)
        html = render_template('reset.html', confirm_url=confirm_url)
        subject = "Link for Resetting your Password"
        msg = Message("Open Source Platform | Password Reset",
                      recipients=[email],
                      html=html)
        mail.send(msg)

        # Inform the user that a confirmation email has been sent
        flash('A password reset email has been sent.', 'success')

        # Redirect to the unconfirmed webpage
        return redirect(url_for('auth.password_reset_email'))
        
    # Render the signup page
    else:
        return render_template('password_reset_email.html',
                               title='OSP | Email Password Reset')
    
# Route used for confirming account using token emailed to user
@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):

    # Attempt to confirm the token and retrieve the email used to generate it
    try:
        email = confirm_token(token)

    # If the token fails to be confirmed, report it to the user
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    # Find user by the email taken from token
    user = Users.query.filter_by(email=email).first_or_404()

    # If the email is already confirmed, report it to the user
    if user.confirmed:
        flash('Account already confirmed.', 'success')

    # If the email is not already confirmed, confirm it
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now(),
        db.session.add(user)
        db.session.commit()
        flash('Account confirmed. Thanks!', 'success')

    # redirect to main profile
    return redirect(url_for('main.profile'))

# Route used for handling forgetting a password
@auth.route('/forgot-password/<token>')
def forgot_password(token):

    # Attempt to confirm the token and retrieve the email used to generate it
    try:
        email = confirm_token(token)

    # If the token fails to be confirmed, report it to the user
    except:
        flash('The "forgot password" link is invalid or has expired.', 'danger')

    # Find user by the email taken from token
    user = Users.query.filter_by(email=email).first_or_404()

    # Allow the user to reset via the reset_password route
    user.reset = True
    db.session.add(user)
    db.session.commit()
    
    # If the email is not confirmed, the user may not reset their password
    if not user.confirmed:
        flash('Account must be confirmed in order to reset password.', 'danger')
        return redirect(url_for('auth.login'))

    # Login the user
    login_user(user)
    
    # redirect to reset password
    return redirect(url_for('auth.reset_password'))

# Route for resetting a password
@auth.route('/reset_password', methods=['GET', 'POST'])
@login_required
@check_confirmed
@check_reset
def reset_password():

    # Logic for changing a user's password
    if request.method == 'POST'  and 'password_change' in request.form:

        # Get the old and new password from the form
        new_pass = request.form.get('password_change')

        # Update the current user's password
        user = current_user
        password = generate_password_hash(new_pass, method='sha256')
        user.password = password
        user.reset = False
        db.session.add(user)
        db.session.commit()
        
        # flash name change message
        flash('Password Reset')
        
        # Load the manage page
        return redirect(url_for('main.profile'))
        
    # Render the password reset page
    else:
        return render_template('reset_password.html', title='OSP | Reset Password')

# Route for the unconfirmed user webpage
@auth.route('/unconfirmed')
@login_required
def unconfirmed():

    # If user is confirmed, redirect to the homepage
    if current_user.confirmed:
        return redirect(url_for('index'))

    # Prompt the user to confirm their account
    flash('Please confirm your account!', 'warning')

    # Render the unconfirmed webpage
    return render_template('unconfirmed.html', title='OSP | Please Confirm')

# Route for resending a confirmation token
@auth.route('/resend')
@login_required
def resend_confirmation():

    # Generate a new token using the user's email
    token = generate_confirmation_token(current_user.email)

    # Generate the email message and send it
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    msg = Message("Open Source Platform | Signup Confirmation",
                  recipients=[current_user.email],
                  html=html)
    mail.send(msg)

    # Inform the user that a confirmation email has been sent
    flash('A new confirmation email has been sent.', 'success')

    # Redirect to the unconfirmed webpage
    return redirect(url_for('auth.unconfirmed'))

# Route for managing profile details
@auth.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():

    # Logic for changing a user's name
    if request.method == 'POST'  and 'name_change' in request.form:

        # Get the new name from the form
        name = request.form.get('name_change')

        # Update the current user's name
        user = current_user
        user.name = name
        db.session.add(user)
        db.session.commit()
    
        # flash name change message
        flash('Name changed to ' + name)
        
        # Load the manage page
        return redirect(url_for('auth.manage'))

    elif request.method == 'POST'  and 'email_change' in request.form:

        # Get the data from the form
        email = request.form.get('email_change')

        # Check if the user's email already belongs to an account
        q = db.session.query(Users.id).filter(Users.email==email)

        # If the user's email exists, email change fails
        if db.session.query(q.exists()).scalar():
            flash('Email address already exists')
            return redirect(url_for('auth.manage'))

        # Generate the user's token and create the email content
        token = generate_confirmation_token(email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('email_change.html', confirm_url=confirm_url)
        
        # Update the current user's email
        user = current_user
        user.email = email
        user.confirmed = False
        db.session.add(user)
        db.session.commit()

        # Craft the confirmation email and send it
        msg = Message("Open Source Platform | Email Change",
                      recipients=[email],
                      html=html)
        mail.send(msg)

        # flash sign up message
        flash('Email changed to ' + email + ', please use the link sent ' + \
              'to this email to confirm your account.')
        
        # Load the manage page
        return redirect(url_for('auth.manage'))

    elif request.method == 'POST'  and 'password_change' in request.form:

        # Get the old and new password from the form
        old_pass = request.form.get('password_old')
        new_pass = request.form.get('password_change')

        # If the password is incorrect, authentication fails
        if not check_password_hash(current_user.password, old_pass):
            
            # Inform the user that their login has failed
            flash('Please check your previous password and try again.')
            return redirect(url_for('auth.manage'))
        
        # Update the current user's password
        user = current_user
        password = generate_password_hash(new_pass, method='sha256')
        user.password = password
        db.session.add(user)
        db.session.commit()
    
        # flash name change message
        flash('Password Updated')
        
        # Load the manage page
        return redirect(url_for('auth.manage'))
        
    # Render the management webpage
    else:
        return render_template('manage.html', title='OSP | Account Management')

# Route for deleting your account
@auth.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():

    # Logic for deleting a user
    if request.method == 'POST'  and 'delete' in request.form:

        # Delete the user's favorites
        Favorites.query.filter(Favorites.user_id == current_user.id).delete()

        # Delete the user
        Users.query.filter(Users.id == current_user.id).delete()
        db.session.commit()
        
        # Log out the user and return to homepage
        logout_user()

        # Flash log out message
        flash('Successfully deleted account')
    
        return redirect(url_for('index'))
        
    # Render the account deletion webpage
    return render_template('delete.html', title='OSP | Delete your Account')
    
# Route for logging out
@auth.route('/logout')
@login_required
def logout():

    # Log out the user and return to homepage
    logout_user()

    # Flash log out message
    flash('Successfully logged out')
    
    return redirect(url_for('index'))
