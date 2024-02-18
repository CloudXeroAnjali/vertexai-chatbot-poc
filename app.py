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

retriever = GoogleVertexAISearchRetriever(
    project_id=PROJECT_ID,
    location_id=DATA_STORE_LOCATION,
    data_store_id=DATA_STORE_ID,
    get_extractive_answers=True,
    max_documents=40,
    max_extractive_segment_count=1,
    max_extractive_answer_count=5,
)

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import GoogleVertexAIMultiTurnSearchRetriever

multi_turn_retriever = GoogleVertexAIMultiTurnSearchRetriever(
    project_id=PROJECT_ID, location_id=DATA_STORE_LOCATION, data_store_id=DATA_STORE_ID
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversational_retrieval = ConversationalRetrievalChain.from_llm(
    llm=llm, retriever=multi_turn_retriever, memory=memory
)

def create_session():
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()
    return chat

def response(chat, message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    result = chat.send_message(message, **parameters)
    return result.text

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
    chat_model = create_session()
    
    result = conversational_retrieval({"question": search_query})
    #content = response(chat_model,user_input)
    return jsonify(content=result)

if __name__ == '__main__':
    app.run(debug=True)#, port=8000, host='0.0.0.0')