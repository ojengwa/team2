# A very simple Flask Hello World app for you to get started with...
import os
from flask import Flask, g, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext import restful
#from flask.ext.restful import reqparse, Api
from flask.ext.wtf import Form
from marshmallow import Serializer, fields
from wtforms.validators import Email
from werkzeug import generate_password_hash, check_password_hash
from wtforms_alchemy import model_form_factory
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % os.path.join(basedir, 'blog.sqlite')
app.debug = True
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
# flask-restful
api = restful.Api(app)


# Declare Model blueprints used in creating users
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
        self.user_id = request.form['id']

    def __repr__(self):
        return '<Post %r>' % self.title


db.create_all()
# Forms
BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    
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


class UserSerializer(Serializer):
    
    class Meta:
        fields = ("id", "email")


class PostSerializer(Serializer):
    user = fields.Nested(UserSerializer)
    
    class Meta:
        fields = ("id", "title", "body", "user", "created_at")

# Views
@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return check_password_hash(user.password, password)


class UserView(restful.Resource):

    def post(self):
        form = UserCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return UserSerializer(user).data


class SessionView(restful.Resource):

    def post(self):
        form = SessionCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            return UserSerializer(user).data, 201
        return '', 401


class PostListView(restful.Resource):
    """Over rest we all only get request for to retrieve all posts"""
    def get(self):
        """Retrieve all posts and return as json object"""
        posts = Post.query.all()
        return PostSerializer(posts, many=True).data

    @auth.login_required
    def post(self):
        form = PostCreateForm()
        if not form.validate_on_submit():
            return form.errors, 422
        post = Post(form.title.data, form.body.data)
        db.session.add(post)
        db.session.commit()
        return PostSerializer(post).data, 201


class PostView(restful.Resource):
    def get(self, id):
        posts = Post.query.filter_by(id=id).first()
        return PostSerializer(posts).data

# Add resource to api
api.add_resource(UserView, '/api/v1/users')
api.add_resource(SessionView, '/api/v1/sessions')
api.add_resource(PostListView, '/api/v1/posts')
api.add_resource(PostView, '/api/v1/posts/<int:id>')