from flask import Flask, Response, jsonify, request
from app.utils.SHModelUtils import *

app = Flask(__name__)

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

        match codeLanguage:
            case 'PYTHON3':
                # pythonModel.persist_model()
                pythonModel = SHModel(PYTHON3_LANG_NAME, "python_model_latest")
                pythonModel.setup_for_prediction()
                prediction = pythonModel.predict(tokenIds)

                return jsonify(hCodes = prediction)

            case 'JAVA':
                javaModel = SHModel(JAVA_LANG_NAME, 'java_model_latest')
                javaModel.setup_for_prediction()
                prediction = javaModel.predict(tokenIds)

                return jsonify(hCodes = prediction)

            case 'KOTLIN':
                kotlinModel = SHModel(KOTLIN_LANG_NAME, 'kotlin_model_latest')
                kotlinModel.setup_for_prediction()
                prediction = kotlinModel.predict(tokenIds)
                return jsonify(hCodes = prediction)

    else:
        return 'Content-Type is not supported!'

# Use this endpoint to pull best model from mongo and call setu_up_for_prediction
# Check if there's a downtime
@app.route('/update', methods=['POST'])
def pull_latest_model():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)

