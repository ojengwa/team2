import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % os.path.join(basedir, 'blog.sqlite')
app.debug = True
app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)

auth = HTTPBasicAuth()

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email