from flask import Flask, jsonify, abort

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)