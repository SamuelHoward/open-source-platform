from flask_app import db

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
    
    def __repr__(self):
        return 'Project: Name: %s URL: %s Description: %s Source: %s Owner: %s Language %s' % (self.name, self.url, self.description, self.source, self.owner, self.language)

class Organizations(db.Model):

    name = db.Column(db.String(80), primary_key=True)
    url = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    
    def __repr__(self):
        return 'Organization: Name: %s URL: %s' % (self.name, self.url)
