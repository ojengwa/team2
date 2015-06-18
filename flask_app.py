import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from werkzeug import generate_password_hash, check_password_hash
from wtforms import StringField
from wtforms.validators import DataRequired


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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()

# All forms to inherit from the WTF Form class
BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    """We use this to bind all forms to our database"""
    @classmethod
    def get_session(cls):
        return db.session


class UserCreateForm(ModelForm):
    class Meta:
        model = User


class SessionCreateForm(Form):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class PostCreateForm(ModelForm):
    class Meta:
        model = Post

