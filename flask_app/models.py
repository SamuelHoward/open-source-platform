from flask_app import db

class Projects(db.Model):

    name = db.Column(db.String(80), primary_key=True)
    url = db.Column(db.String(100))
    description = db.Column(db.String(500))
    source = db.Column(db.String(32))
    owner = db.Column(db.String(32))
    language = db.Column(db.String(32))
    
    def __repr__(self):
        return 'Project: Name: %s URL: %s Description: %s Source: %s Owner: %s Language %s' % (self.name, self.url, self.description, self.source, self.owner, self.language)
