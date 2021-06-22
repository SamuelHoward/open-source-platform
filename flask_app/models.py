from flask_app import db
from flask_login import UserMixin

class Projects(db.Model):

    name = db.Column(db.String(80), primary_key=True)
    url = db.Column(db.String(100))
    description = db.Column(db.String(500))
    source = db.Column(db.String(32))
    owner = db.Column(db.String(32))
    owner_avatar = db.Column(db.String(100))
    language = db.Column(db.String(32))
    created_time = db.Column(db.String(32))
    last_updated = db.Column(db.String(32))
    forks = db.Column(db.Integer)
    watchers = db.Column(db.Integer)
    open_issues = db.Column(db.Integer)
    owner_type = db.Column(db.String(32))
    
    def __repr__(self):
        return 'Project: Name: %s URL: %s Description: %s Source: %s Owner: %s Language %s' % (self.name, self.url, self.description, self.source, self.owner, self.language)
    
class Organizations(db.Model):
        
    name = db.Column(db.String(80), primary_key=True)
    url = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    owner_type = db.Column(db.String(32))
    
    def __repr__(self):
        return 'Organization: Name: %s URL: %s' % (self.name, self.url)

class Users(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
