from flask import Flask, jsonify, request
from app.utils.SHModelUtils import *
from app.services.ModelService import *

app = Flask(__name__)

def load_python_model():
    python_model: SHModel = load_model_from_db('latest', 'PYTHON3')
    python_model.setup_for_prediction()
    return python_model

def load_java_model():
    java_model: SHModel = load_model_from_db('latest', 'JAVA')
    java_model.setup_for_prediction()
    return java_model

def load_kotlin_model():
    kotlin_model: SHModel = load_model_from_db('latest', 'KOTLIN')
    kotlin_model.setup_for_prediction()
    return kotlin_model

# Loading models for supported languages
python_model = load_python_model()
java_model = load_java_model()
kotlin_model = load_kotlin_model()


@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting prediction api'})


@app.route('/predict', methods=['POST'])
def predict():

    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        requestBody = request.json
        codeLanguage = requestBody['codeLanguage']
        tokenIds = requestBody['tokenIds']

        if codeLanguage == 'PYTHON3':
            prediction = python_model.predict(tokenIds)
            return jsonify(prediction = prediction)

        elif codeLanguage == 'JAVA':
            prediction = java_model.predict(tokenIds)
            return jsonify(prediction = prediction)

        elif codeLanguage == 'KOTLIN':
            prediction = kotlin_model.predict(tokenIds)
            return jsonify(prediction = prediction)

    else:
        return 'Content-Type is not supported!'

# Use this endpoint to pull best model from mongo and call setu_up_for_prediction
# Check if there's a downtime
@app.route('/update', methods=['POST'])
def pull_latest_model():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)

