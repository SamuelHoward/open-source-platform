from flask_app import db

class Projects(db.Model):

    name = db.Column(db.String(80), primary_key=True)
    url = db.Column(db.String(100))
    description = db.Column(db.String(500))
    source = db.Column(db.String(32))
    
    def __repr__(self):
        return 'Project: Name: %s URL: %s Description: %s Source: %s' % (self.name, self.url, self.description, self.source)
