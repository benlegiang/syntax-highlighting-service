from app.services.MongoDatabase import MongoDatabase
import pickle
from app.utils.SHModelUtils import SHModel
import requests

class ModelService:

    def __init__(self, database: str, training_api: str):
        self.client = MongoDatabase().client
        self.database = database
        self.training_api = training_api
        # Loads for each language its model from the database stored as binary
        self.python_model: SHModel = self.load_model_from_db('PYTHON3', None)
        self.java_model: SHModel = self.load_model_from_db('JAVA', None)
        self.kotlin_model: SHModel = self.load_model_from_db('KOTLIN', None)


    def setup_models_for_prediction(self):

        # Sets up every model for prediction
        self.python_model.setup_for_prediction()
        self.java_model.setup_for_prediction()
        self.kotlin_model.setup_for_prediction()

    def pull_latest_model(self, model_lang: str, model_number: int):
        if model_lang == 'PYTHON3':
            self.python_model = self.load_model_from_db(model_lang, model_number)

        elif model_lang == 'JAVA':
            self.java_model = self.load_model_from_db(model_lang, model_number)
        
        elif model_lang == 'KOTLIN':
            self.kotlin_model = self.load_model_from_db(model_lang, model_number)

    def check_if_model_exists(self, model_lang):
        try:
            db = self.client[self.database]

            collection = db[model_lang]

            if collection.count_documents({}) > 0:
                return True
            else:
                return False
        except:
            print("Error: Unable to establish database connection")

    def get_model_data(self, model_number: int, model_lang: str):
        json_data = {}

        db = self.client[self.database]
        collection = db[model_lang]

        document = collection.find({"modelNumber": model_number})
        
        for i in document:
            json_data = i

        pickled_model = json_data['modelData']

        print(f'[SUCCESS]: Loaded model {model_number} for {model_lang}')
        return pickle.loads(pickled_model)   

    def get_latest_model_number(self, model_lang: str):
        db = self.client[self.database]

        collection = db[model_lang]

        size = collection.count_documents({})

        return size   

    # Returns a model
    def load_model_from_db(self, model_lang: str, model_number: int) -> SHModel:
        try: 
            if model_number == None and self.check_if_model_exists(model_lang):
                latest = self.get_latest_model_number(model_lang)
                return self.get_model_data(latest, model_lang)

            else:
                # Make request to training.api for it to init training of very first model and save it to DB

                request = requests.post(self.training_api + f'/build?lang={model_lang}').json()

                if request['success'] == True and request['modelNumber']:
                    return self.get_model_data(request['modelNumber'], model_lang)

        except Exception as e: 
            print(f'Error: Unable to load model - ', e)
            return None


