import pickle
from datetime import datetime
import random
from app.utils.SHModelUtils import JAVA_LANG_NAME, KOTLIN_LANG_NAME, PYTHON3_LANG_NAME, SHModel
from app.utils.services.MongoDatabase import MongoDatabase

class ModelService:

    def __init__(self, database: str, collection: str, model_lang: str, batch_size: int, training_size: float):
        self.database = database
        self.collection = collection
        self.batch_size = batch_size
        self.training_size = training_size
        self.model_number = 0

        self.setup_model(model_lang)

    def setup_model(self, model_lang: str):

        if model_lang == 'PYTHON3':
            self.model_number = self.get_model_number(model_lang)
            print(self.model_number)

            model = SHModel(PYTHON3_LANG_NAME, f'model_{self.model_number}')
            model.setup_for_finetuning()
            # Skip fine-tuning of very first model
            if self.model_number != 0:
                self.fine_tune_model(model, self.model_number, model_lang)
            else:
                self.save_model_to_db(model, self.model_number, model_lang, 0, 0, 0, 100)

        elif model_lang == 'JAVA':
            self.model_number = self.get_model_number(model_lang)
            print(self.model_number)
            model = SHModel(JAVA_LANG_NAME, f'model_{self.model_number}')
            model.setup_for_finetuning()
            if self.model_number != 0:
                self.fine_tune_model(model, self.model_number, model_lang)
            else:
                self.save_model_to_db(model, self.model_number, model_lang, 0, 0, 0, 100)
        
        elif model_lang == 'KOTLIN':
            self.model_number = self.get_model_number(model_lang)
            print(self.model_number)

            model = SHModel(KOTLIN_LANG_NAME, f'model_{self.model_number}')
            model.setup_for_finetuning()
            if self.model_number != 0:
                self.fine_tune_model(model, self.model_number, model_lang)
            else:
                self.save_model_to_db(model, self.model_number, model_lang, 0, 0, 0, 100)

    def get_model_number(self, model_lang: str):
        client = MongoDatabase().client

        db = client[self.database]

        collection = db[model_lang]

        size = collection.count_documents({})

        return size + 1

    def save_model_to_db(self, model: SHModel, model_number: int, model_lang: str, training_size: int, test_size: int, accuracy: float, loss: float):
        client = MongoDatabase().client

        model.persist_model()
        try:
            pickled_model = pickle.dumps(model)

            db = client[self.database]
            collection = db[model_lang]

            query = collection.insert_one({"modelNumber": model_number, "modelData": pickled_model, "trainingSize": training_size, "testSize": test_size, "accuracy": accuracy, "loss": loss, "createdAt": datetime.now().isoformat()})
        
            details = {'insertedId': query.inserted_id, "createdAt": datetime.now().isoformat()}

            return details
        except Exception as e: 
            print(e)
            return 'Saving model to database failed'


    def load_annotations_from_db(self, code_lang):

        client = MongoDatabase().client

        try:
            db = client[self.database]
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
            print(e)
            return 'Loading annotations from database failed'


    def fine_tune_model(self, model: SHModel, model_number: int, model_lang: str):

        try: 
            annotations = self.load_annotations_from_db(model_lang)

            loss = 0

            random.shuffle(annotations)

            train_data = annotations[:int((len(annotations)+1)*self.training_size)]
            test_data = annotations[int((len(annotations)+1)*self.training_size):]

            for annotation in train_data:
                loss = model.finetune_on(annotation['tokenIds'], annotation['formal'])

            test_ids = [test.get('_id') for test in test_data]

            # Set up for prediction to measure accuracy of fine-tuning
            model.setup_for_prediction()
            
            total_items = len(test_data)
            correct = 0
            print("Predicting...")

            accuracy = None
            for annotation in test_data:
                p = model.predict(annotation['tokenIds'])
                if p == annotation['formal']:
                    correct += 1

                accuracy = correct / total_items * 100

                client = MongoDatabase().client

                db = client[self.database]
                collection = db[self.collection]

                query = {'_id': {'$in': test_ids}}
                update = {'$set': {'isTestItem': True}}

                collection.update_many(query, update)

            self.save_model_to_db(model, model_number, model_lang, len(train_data), len(test_data), accuracy, loss)

        except Exception as e:
            print(e)





