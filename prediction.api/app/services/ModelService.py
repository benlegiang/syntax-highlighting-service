from app.services.MongoDatabase import MongoDatabase
import pickle
from app.utils.SHModelUtils import SHModel
import requests

class ModelService:

    def __init__(self, database: str, training_api: str):
        self.database = database
        self.training_api = training_api
        # Loads for each language its model from the database stored as binary
        self.python_model: SHModel = self.load_model_from_db(1, 'PYTHON3')
        self.java_model: SHModel = self.load_model_from_db(1, 'JAVA')
        self.kotlin_model: SHModel = self.load_model_from_db(1, 'KOTLIN')

        self.setup_models_for_prediction()

    def setup_models_for_prediction(self):

        # Sets up every model for prediction
        self.python_model.setup_for_prediction()
        self.java_model.setup_for_prediction()
        self.kotlin_model.setup_for_prediction()

    def check_if_model_exists(self, model_lang):
        try:
            client = MongoDatabase().client
            
            db = client[self.database]

            collection = db[model_lang]

            if collection.count_documents({}) > 0:
                return True
            else:
                return False
        except:
            print("Error: Unable to establish database connection")

    # Returns a model
    def load_model_from_db(self, model_number, model_lang: str) -> SHModel:
        try:
            if self.check_if_model_exists(model_lang):
                json_data = {}

                client = MongoDatabase().client

                db = client[self.database]

                collection = db[model_lang]

                document = collection.find({"modelNumber": model_number})

                for i in document:
                    json_data = i
                pickled_model = json_data['modelData']

                print(f'Success: Loaded model for {model_lang} from DB')

                return pickle.loads(pickled_model)

            else:
                # Make request to training.api for it to init train very first model and save it to DB

                request = requests.post(self.training_api + f'?lang={model_lang}').json()
                print(request)

                if request['success'] == True and request['modelNumber']:
                    try:
                        json_data = {}

                        client = MongoDatabase().client

                        db = client[self.database]

                        collection = db[model_lang]

                        document = collection.find({"modelNumber": request['modelNumber']})
                        print(document)

                        for i in document:
                            json_data = i
                        pickled_model = json_data['modelData']

                        print(f'Success: Loaded model for {model_lang} from DB')

                        return pickle.loads(pickled_model)

                    except:
                        print(f'Error: {model_lang} model does not exist yet!')
                        return None

        except Exception as e: 
            print(f'Error: Unable to load model - ', e)
            return None



