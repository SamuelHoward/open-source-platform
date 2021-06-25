from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db?check_same_thread=False'
app.config['SECRET_KEY'] = '31773cfeb73cf71ada270055544a909d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import Users

@login_manager.user_loader
def load_user(user_id):
    #print(user_id)
    if user_id is not None and user_id != 'None':
        #print(type(user_id))
        return Users.query.get(int(user_id))

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

# from flask_app import routes
from flask_app.models import *
