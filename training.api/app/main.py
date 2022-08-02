import code
from flask import Flask, jsonify, request
from pymongo import MongoClient
import pickle
from datetime import datetime
from app.utils.SHModelUtils import *

app = Flask(__name__)
mongoUri = 'mongodb://admin:admin@localhost:27017'
database = 'syntaxHighlighting'
batch_size = 10


def setup_python_model():
    python_model = SHModel(PYTHON3_LANG_NAME, "model_latest")
    python_model.setup_for_finetuning()

    return python_model
def setup_java_model():
    java_model = SHModel(JAVA_LANG_NAME, "model_latest")
    java_model.setup_for_finetuning()

    return java_model

def setup_kotlin_model():
    kotlin_model = SHModel(KOTLIN_LANG_NAME, "model_latest")
    kotlin_model.setup_for_finetuning()

    return kotlin_model

python_model = setup_python_model()
java_model = setup_java_model()
kotlin_model = setup_kotlin_model()


@app.route("/", methods=['GET', 'POST'])
def index():

    return jsonify({'message':'syntax highlighting training api'})

@app.route('/training', methods=['POST'])
def train():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        request_body = request.json
        code_language = request_body['codeLanguage']
        token_ids = request_body['tokenIds']
        h_code_values = request_body['hCodeValues']

        print(h_code_values)
        if code_language == 'PYTHON3':
            loss = python_model.finetune_on(token_ids, h_code_values)
            return jsonify(l = loss)

        elif code_language == 'JAVA':
            loss = java_model.finetune_on(token_ids, h_code_values)
            return jsonify(l = loss)

        elif code_language == 'KOTLIN':
            loss = kotlin_model.finetune_on(token_ids, h_code_values)
            return jsonify(l = loss)
    else:
        return 'Content-Type is not supported!'


# Save model
def save_model_to_db(model, model_lang):
    client = MongoClient(mongoUri)
    # client = MongoClient('mongodb://admin:admin@mongodb:27017')
    try:
        pickled_model = pickle.dumps(model)

        db = client[database]
        collection = db[model_lang]

        response = collection.insert_one({"model": pickled_model, "created_at": datetime.now().isoformat()})

        # print(response.inserted_id, ' saved successfully')
    
        details = {'inserted_id': response.inserted_id, "created_at": datetime.now().isoformat()}

        return details
    except: 
        return 'Saving model to database failed'

# Returns a model
def load_model_from_db(model_name, model_lang):

    try:
        json_data = {}

        client = MongoClient(mongoUri)

        db = client[database]

        collection = db[model_lang]

        document = collection.find({"name": ""})

        # for i in document:
        #     json_data = i
        # pickled_model = json_data[model]

        # return pickle.loads(pickled_model)

        return None
    except:
        return 'Loading model from database failed'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8001)

# export FLASK_APP=app.main:app
# export FLASK_ENV=development

