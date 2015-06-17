from flask import Flask
from models import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
import views

db.init_app(app)

