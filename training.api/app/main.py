from flask import Flask, jsonify, request

from app.utils.SHModelUtils import *
from app.utils.services.ModelService import ModelService
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

prediction_api = 'http://syntax-highlighting-service-load-balancer:7777/api/v1'
database: str = 'syntaxHighlighting'
annotations_collection: str = 'annotations'
batch_size: int = 20000
training_size: float = 0.8
check_db_interval: int = 5 
threshold = 100

modelService = ModelService(prediction_api, database, annotations_collection, batch_size, training_size)

# Scheduler for checking changes to DB

scheduler = BackgroundScheduler()

scheduler.add_job(modelService.check_db_changes, 'interval', minutes=check_db_interval, args=(database, annotations_collection, threshold))
scheduler.start()

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting training api'})
    

# Endpoint is only called once to initiate empty models
@app.route("/api/v1/build", methods=['POST'])
def build_model():
    model_lang: str = request.args.get('lang').upper()
    try:
        model_number = modelService.build_model(model_lang)
        return jsonify({'success': True, 'modelLang': model_lang, 'modelNumber': model_number})

    except Exception as e: 
        return jsonify({'success': False, 'message': e })

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8001)