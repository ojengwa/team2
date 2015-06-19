from flask import Flask, jsonify, abort, request, abort
from blog import app
from models import db
import re

posts = [
            {
            'id': 1,
            'title': u'Buy groceries',
            'content': u'Milk, Cheese, Pizza, Fruit, Tylenol',
            'date': u'13 Jun 05',
            'num_comment': 0,
            'author': 1
            },
            {
            'id': 2,
            'title': u'Learn Python',
            'content': u'Need to find a good Python tutorial on the web',
            'date': u'14 Jun 10',
            'num_comment': 2,
            'author': 1
            }
        ]
comments = [
                {
                'id': 1,
                'content': u'Love this stuff',
                'date': u'12 Jun 05',
                'author': 1
                }
            ]

# Helper function to generate slug
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))

@app.route('/', methods=['GET'])
def index():
    return jsonify({'posts':posts})

@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    """Read Post by Id"""
    id = int(post_id)
    return jsonify({'post':posts[id], 'comments':comments})

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}, 
                    201, 
                    {'Location': url_for('get_user', id = user.id, _external = True)})