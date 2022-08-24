from lib2to3.pygram import python_symbols
import pickle
from datetime import datetime
import random
import time
from app.utils.SHModelUtils import JAVA_LANG_NAME, KOTLIN_LANG_NAME, PYTHON3_LANG_NAME, SHModel
from app.utils.services.MongoDatabase import MongoDatabase
import logging
import requests

logging.basicConfig(filename="logs.txt")

class ModelService:

    def __init__(self, prediction_api: str, database: str, collection: str, batch_size: int, training_size: float):
        self.client = MongoDatabase().client
        self.prediction_api = prediction_api
        self.database = database
        self.collection = collection
        self.batch_size = batch_size
        self.training_size = training_size
        
        self.python3_size = 0
        self.java_size = 0
        self.kotlin_size = 0

    def build_deploy_model(self,model_lang: str):
        model_number = self.build_model(model_lang)
        self.trigger_model_pull(model_lang, model_number)

    def trigger_model_pull(self, model_lang: str, model_number: int):
        requests.post(self.prediction_api + f'/deploy?lang={model_lang}&no={model_number}')

    def build_model(self, model_lang: str):
        if model_lang == 'PYTHON3':
            model_number = self.get_latest_model_number(model_lang) + 1
            model = SHModel(PYTHON3_LANG_NAME, f'model_{model_number}')
            model.setup_for_finetuning()
            # Skip fine-tuning of very first model
            if model_number != 1:
                self.fine_tune_model(model, model_number, model_lang)
            else:
                self.save_model_to_db(model, model_number, model_lang, 0, 0, 0, 100)

            return model_number

        elif model_lang == 'JAVA':
            model_number = self.get_latest_model_number(model_lang) + 1
            model = SHModel(JAVA_LANG_NAME, f'model_{model_number}')
            model.setup_for_finetuning()
            if model_number != 1:
                self.fine_tune_model(model, model_number, model_lang)
            else:
                self.save_model_to_db(model, model_number, model_lang, 0, 0, 0, 100)
            
            return model_number

        
        elif model_lang == 'KOTLIN':
            model_number = self.get_latest_model_number(model_lang) + 1
            model = SHModel(KOTLIN_LANG_NAME, f'model_{model_number}')
            model.setup_for_finetuning()
            if model_number != 1:
                self.fine_tune_model(model, model_number, model_lang)
            else:
                self.save_model_to_db(model, model_number, model_lang, 0, 0, 0, 100)
            return model_number

    def get_latest_model_number(self, model_lang: str):
        db = self.client[self.database]

        collection = db[model_lang]

        size = collection.count_documents({})

        return size

    def save_model_to_db(self, model: SHModel, model_number: int, model_lang: str, training_size: int, test_size: int, accuracy: float, loss: float):
        model.persist_model()
        try:
            pickled_model = pickle.dumps(model)

            db = self.client[self.database]
            collection = db[model_lang]

            query = collection.insert_one({"modelNumber": model_number, "modelData": pickled_model, "trainingSize": training_size, "testSize": test_size, "accuracy": accuracy, "loss": loss, "createdAt": datetime.now().isoformat()})
        
            details = {'insertedId': query.inserted_id, "createdAt": datetime.now().isoformat()}

            return details
        except Exception as e: 
            logging.error(e)
            return 'Saving model to database failed'


    def load_annotations_from_db(self, code_lang):

        try:
            db = self.client[self.database]
            collection = db[self.collection]

            annotations_query = collection.aggregate([

                {
                    '$match': {'codeLanguage': code_lang, 'isTrainable': True}
                },

                {
                    "$sample": {'size': self.batch_size}
                },
                
            ])

            annotations = []

            for annotation in annotations_query:
                annotations.append(annotation)

            return annotations

        except Exception as e:
            logging.error(e)
            return 'Loading annotations from database failed'


    def fine_tune_model(self, model: SHModel, model_number: int, model_lang: str):

        try: 
            annotations = self.load_annotations_from_db(model_lang)

            train_data = annotations[:int((len(annotations)+1)*self.training_size)]
            test_data = annotations[int((len(annotations)+1)*self.training_size):]

            loss = None
            accuracy = None
            training_size = len(train_data)
            test_size = len(test_data)
            

            random.shuffle(annotations)


            for annotation in train_data:
                loss = model.finetune_on(annotation['tokenIds'], annotation['formal'])

            test_ids = [test.get('_id') for test in test_data]

            # Set up for prediction to measure accuracy of fine-tuning
            model.setup_for_prediction()
            
            correct = 0
            accuracy = None

            for annotation in test_data:
                p = model.predict(annotation['tokenIds'])
                if p == annotation['formal']:
                    correct += 1

                accuracy = correct / test_size * 100

                db = self.client[self.database]
                collection = db[self.collection]

                query = {'_id': {'$in': test_ids}}
                update = {'$set': {'isTestItem': True}}

                collection.update_many(query, update)

            # TODO: Only save to DB if it actually improved!!!!!!!!!!
            # See ConUpdate/Reuse
            self.save_model_to_db(model, model_number, model_lang, training_size, test_size, accuracy, loss)

        except Exception as e:
            logging.error(e)

    def check_db_changes(self, database: str, annotations_collection: str, threshold: int): 
        db = self.client[database]
        collection = db[annotations_collection]

        python3_size = collection.count_documents({'codeLanguage': 'PYTHON3', 'isTrainable': True, 'isTestItem': False})
        java_size = collection.count_documents({'codeLanguage': 'JAVA', 'isTrainable': True, 'isTestItem': False})
        kotlin_size = collection.count_documents({'codeLanguage': 'KOTLIN', 'isTrainable': True, 'isTestItem': False})

        python3_model_number_latest = self.get_latest_model_number('PYTHON3') 
        java_model_number_latest = self.get_latest_model_number('JAVA') 
        kotlin_model_number_latest = self.get_latest_model_number('KOTLIN')

        if python3_model_number_latest > 0:
            if python3_size - self.python3_size > threshold and python3_size != 0:
                self.build_model('PYTHON3')
                # Re-count due to changes caused by splitting data sets
                self.python3_size = collection.count_documents({'codeLanguage': 'PYTHON3', 'isTrainable': True, 'isTestItem': False})
        
        if java_model_number_latest > 0:
            if java_size - self.java_size > threshold and java_size != 0:
                self.build_model('JAVA')
                self.java_size = collection.count_documents({'codeLanguage': 'JAVA', 'isTrainable': True, 'isTestItem': False})

        if kotlin_model_number_latest > 0:
            if kotlin_size - self.kotlin_size > threshold and kotlin_size != 0:
                self.build_model('KOTLIN')
                print("Success: Built Kotlin model")
                self.kotlin_size = collection.count_documents({'codeLanguage': 'KOTLIN', 'isTrainable': True, 'isTestItem': False})





