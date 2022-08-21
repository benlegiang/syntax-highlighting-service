from flask import Flask, jsonify, request
from app.utils.SHModelUtils import *
from app.services.ModelService import *

app = Flask(__name__)

database = 'syntaxHighlighting'
# training_api = 'http://localhost:8001/init'
training_api = 'http://syntax-highlighting-service-training-api:8001/init'
modelService = ModelService(database, training_api)

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
            prediction = modelService.python_model.predict(tokenIds)
            return jsonify(prediction = prediction)

        elif codeLanguage == 'JAVA':
            prediction = modelService.java_model.predict(tokenIds)
            return jsonify(prediction = prediction)

        elif codeLanguage == 'KOTLIN':
            prediction = modelService.kotlin_model.predict(tokenIds)
            return jsonify(prediction = prediction)

    else:
        return 'Content-Type is not supported!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)

