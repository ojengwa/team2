from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'tosin'}
    posts = [  
        { 
            'author': {'nickname': 'tosin'}, 
            'body': 'What i love about mondays' 
        },
        { 
            'author': {'nickname': 'chidi'}, 
            'body': 'Get rich quick schemes' 
        }
    ]
    return render_template('index.html',title='Home',user=user)