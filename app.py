from flask import Flask, jsonify, abort

app = Flask(__name__)

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

@app.route('/', methods=['GET'])
def index():
    return jsonify({'posts':blog_posts})

@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    """Read Post by Id"""
    id = int(post_id)
    return jsonify({'post':posts[id], 'comments':comments})

if __name__ == '__main__':
    app.run(debug=True)