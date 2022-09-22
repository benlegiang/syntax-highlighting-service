from flask import Flask, jsonify, request
from app.utils.SHModelUtils import *
from apscheduler.schedulers.background import BackgroundScheduler
import docker
from app.services.TrainingService import TrainingService

app = Flask(__name__)

cli = docker.APIClient(base_url='unix://var/run/docker.sock')
all_containers = cli.containers()
prediction_containers = [c for c in all_containers if c['Labels']['com.docker.compose.service'] == 'prediction-api']

database: str = 'syntaxHighlighting'
annotations_collection: str = 'annotations'
min_batch_size: int = 1200
max_batch_size: int = 10000
check_db_interval: int = 3
langs = ['PYTHON3', 'JAVA', 'KOTLIN']

trainingService = TrainingService(langs, prediction_containers, database, annotations_collection, min_batch_size, max_batch_size)

# Scheduler for checking changes to DB

scheduler = BackgroundScheduler()

scheduler.add_job(trainingService.check_for_training, 'interval', minutes=check_db_interval)
scheduler.start()

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting training api'})
    

# Endpoint is only called once to initiate empty models
@app.route("/api/v1/build", methods=['POST'])
def build_model():

    model_lang: str = request.args.get('lang').upper()
    try:
        model_number = trainingService.init_model(model_lang)
        return jsonify({'success': True, 'modelLang': model_lang, 'modelNumber': model_number})

    except Exception as e: 
        return jsonify({'success': False, 'message': e })

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8001)