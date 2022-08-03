from flask import Flask, jsonify, request

from app.utils.SHModelUtils import *
from app.utils.services.ModelService import load_annotations_from_db

app = Flask(__name__)



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


        if code_language == 'PYTHON3':
            loss = python_model.finetune_on(token_ids, h_code_values)
            count = load_annotations_from_db('JAVA')
            return jsonify(l = loss, annotationCount = count)

        elif code_language == 'JAVA':
            loss = java_model.finetune_on(token_ids, h_code_values)
            return jsonify(l = loss)

        elif code_language == 'KOTLIN':
            loss = kotlin_model.finetune_on(token_ids, h_code_values)
            return jsonify(l = loss)
    else:
        return 'Content-Type is not supported!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8001)

# export FLASK_APP=app.main:app
# export FLASK_ENV=development

