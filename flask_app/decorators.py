from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

# Wrapper used for checking current user is confirmed
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)
    
    return decorated_function

# Wrapper used for checking current user can reset their password
# without old password
def check_reset(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.reset is False:
            flash('Logged in users must reset their password via account management', 'warning')
            return redirect(url_for('auth.manage'))
        return func(*args, **kwargs)
    
    return decorated_function
