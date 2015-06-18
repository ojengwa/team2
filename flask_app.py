import os
from flask import Flask

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % os.path.join(basedir, 'blog.sqlite')