from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.language_models import ChatModel
import os

app = Flask(__name__)
PROJECT_ID = "vertex-ai-chatbot-414313"  # @param {type:"string"}
LOCATION = "us-central1"   
DATA_STORE_ID = "vertex-ai-chatbot-dataset_1708011349777"  # @param {type:"string"}
DATA_STORE_LOCATION = "global"  # @param {type:"string"}
REGION = "us-central1"  # @param {type:"string"}
MODEL = "text-bison@001"  # @param {type:"string"}

os.environ["DATA_STORE_ID"] = DATA_STORE_ID
os.environ["PROJECT_ID"] = PROJECT_ID
os.environ["LOCATION_ID"] = DATA_STORE_LOCATION
os.environ["REGION"] = REGION
os.environ["MODEL"] = MODEL

import vertexai
from langchain.llms import VertexAI
from langchain.retrievers import GoogleVertexAISearchRetriever

vertexai.init(project=PROJECT_ID, location=REGION)
llm = VertexAI(model_name=MODEL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    else:
        user_input = request.form['user_input']
    
    #result = conversational_retrieval({"question": user_input})
    #content = response(chat_model,user_input)
    return jsonify(content='')

if __name__ == '__main__':
    app.run(debug=True)#, port=8000, host='0.0.0.0')
