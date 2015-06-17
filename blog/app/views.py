from flask import g
from flask.ext import restful
 
from server import api, db, flask_bcrypt, auth
from models import User, Post
from forms import UserCreateForm, SessionCreateForm, PostCreateForm
from serializers import UserSerializer, PostSerializer
 
@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.user = user
    return flask_bcrypt.check_password_hash(user.password, password)