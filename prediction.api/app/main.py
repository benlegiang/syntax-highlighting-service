from flask import Flask, jsonify, request
from app.utils.SHModelUtils import *
from app.services.ModelService import *
import docker
import os

app = Flask(__name__)

# Gets information about all running containers
# Needed to know which number of the replica group this container has
cli = docker.APIClient(base_url='unix://var/run/docker.sock')
HOSTNAME = os.environ.get("HOSTNAME")
all_containers = cli.containers()
our_container = [c for c in all_containers if c['Id'][:12] == HOSTNAME[:12]][0]

container_number = int(our_container['Labels']['com.docker.compose.container-number'])

database = 'syntaxHighlighting'
training_api = 'http://syntax-highlighting-service-training-api:8001/api/v1'

modelService = ModelService(database, training_api, container_number)

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting prediction api'})
    


@app.route('/api/v1/predict', methods=['POST'])
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
        # return f'{container_number}'
        return 'Content-Type is not supported!'
        

@app.route('/api/v1/deploy', methods=['POST'])
def deploy_latest_model():
    model_lang: str = request.args.get('lang').upper()
    model_number: int = int(request.args.get('no'))
    try:
        modelService.pull_latest_model(model_lang, model_number)
        modelService.setup_models_for_prediction()
        return jsonify({'success': True})
 
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Unable to deploy latest model'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
    modelService = ModelService(database, training_api)
    modelService.setup_models_for_prediction()



