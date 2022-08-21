from crypt import methods
from flask import Flask, jsonify, request

from app.utils.SHModelUtils import *
from app.utils.services.ModelService import ModelService

app = Flask(__name__)

database: str = 'syntaxHighlighting'
annotations_collection: str = 'annotations'
batch_size: int = 20000
training_size: float = 0.8

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting training api'})

@app.route("/init", methods=['POST'])
def init_model_training():
    model_lang: str = request.args.get('lang').upper()

    try:
        modelService = ModelService(database, annotations_collection, model_lang, batch_size, training_size)
        return jsonify({'success': True, 'modelLang': model_lang, 'modelNumber': modelService.model_number})

    except Exception as e: 
        return jsonify({'success': False, 'message': e })


@app.route("/build", methods=['POST'])
def build():

    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8001)


