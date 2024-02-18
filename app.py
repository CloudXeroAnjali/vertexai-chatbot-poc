from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.language_models import ChatModel
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
