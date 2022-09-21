from datetime import datetime
import logging
import pickle
from statistics import mean
import requests
from app.utils.SHModelUtils import JAVA_LANG_NAME, KOTLIN_LANG_NAME, PYTHON3_LANG_NAME, SHModel
from app.services.MongoDatabase import MongoDatabase
from threading import Lock
lock = Lock()


class TrainingService:

    def __init__(self, langs: list, prediction_containers: list, database: str, collection: str, min_batch_size: int, max_batch_size):
        self.client = MongoDatabase().client
        self.langs = langs
        self.prediction_containers = prediction_containers
        self.database = database
        self.collection = collection
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        self.training_size = 0.8
        self.epochs = 11
    

    def init_model(self, model_lang: str):
        if model_lang == 'PYTHON3':
            model_number = self.get_latest_model_number(model_lang) + 1
            model = SHModel(PYTHON3_LANG_NAME, f'model_{model_number}')
            self.save_model_to_db(model, model_number, model_lang, 0, 0, 0)
            return model_number

        elif model_lang == 'JAVA':
            model_number = self.get_latest_model_number(model_lang) + 1
            
            model = SHModel(JAVA_LANG_NAME, f'model_{model_number}')
            self.save_model_to_db(model, model_number, model_lang, 0, 0, 0)
            return model_number
        
        elif model_lang == 'KOTLIN':
            model_number = self.get_latest_model_number(model_lang) + 1
            model = SHModel(KOTLIN_LANG_NAME, f'model_{model_number}')

            self.save_model_to_db(model, model_number, model_lang, 0, 0, 0)
            return model_number

    # Checks and attempts a fine-tuning on latest model
    # Lock function from executing, in case training takes longer than the check interval
    def check_for_training(self):
        lock.acquire()
        try:
            for lang in self.langs:
                training_a_unfiltered = self.load_training_annotations(lang)

                if len(training_a_unfiltered) == 0:
                    continue

                # Removes duplicates
                training_a_non_duplicates = self.remove_duplicates(training_a_unfiltered)

                # Not enough training data, skip!
                if len(training_a_non_duplicates) < self.min_batch_size:
                    continue


                # Loads latest model because only model with highest accuracy will be saved to DB anyways
                model_json = self.load_latest_model_from_db(lang)
                
                if model_json == None:
                    continue

                latest_model = self.get_model_data_pickled(model_json)
                latest_model_accuracy = model_json['accuracy']
                latest_model_training_size = int(model_json['trainingSize'])

                # No latest model existing, skip!
                if latest_model == None:
                    continue

                training_data = training_a_non_duplicates[:int((len(training_a_non_duplicates)+1)*self.training_size)]
                validation_data = training_a_non_duplicates[int((len(training_a_non_duplicates)+1)*self.training_size):]

                # input_training = [training_data['hCodeTokenIds'] for training_data['hCodeTokenIds'] in training_data]
                # target_training = [training_data['hCodeValues'] for training_data['hCodeValues'] in training_data]
                input_training = [training['hCodeTokenIds'] for training in training_data]
                target_training = [training['hCodeValues'] for training in training_data]
                
                input_validation = [validation['hCodeTokenIds'] for validation in validation_data]
                target_validation = [validation['hCodeValues'] for validation in validation_data]

                trained_model = self.train_model(latest_model, input_training, target_training)
                trained_accuracy, total_validation_size = self.get_model_accuracy(trained_model, lang, input_validation, target_validation)

                total_training_size = latest_model_training_size + len(training_data)
                
                # If accuracy got better, save model to DB and make all prediction.api instances pull new model
                if trained_accuracy > latest_model_accuracy:
                    new_model_number = self.get_latest_model_number(lang) + 1
                    self.save_model_to_db(trained_model, new_model_number, lang, total_training_size, total_validation_size, trained_accuracy)
                    self.update_training_db_set(training_data)
                    self.update_validation_db_set(validation_data)
                    self.deploy_latest_model(lang, new_model_number)
        finally:
            lock.release()


    # Update training set on DB
    def update_training_db_set(self, training_set):

        ids = [t.get('_id') for t in training_set]
        db = self.client[self.database]
        collection = db[self.collection]
        query = {'_id': {'$in': ids}}
        update = {'$set': {'isTrained': True}}
        collection.update_many(query, update)

    # Update validation set on DB
    def update_validation_db_set(self, validation_set):

        ids = [t.get('_id') for t in validation_set]
        db = self.client[self.database]
        collection = db[self.collection]
        query = {'_id': {'$in': ids}}
        update = {'$set': {'isValidated': True}}
        collection.update_many(query, update)

    # Calculate accuracy for given model
    def get_model_accuracy(self, model: SHModel, lang: str, input_data, target_data):

        old_validation_data = self.load_validation_annotations(lang)

        if len(old_validation_data) != 0:
            # old_input_validation = [old_validation_data['hCodeTokenIds'] for old_validation_data['hCodeTokenIds'] in old_validation_data]
            # old_target_validation = [old_validation_data['hCodeValues'] for old_validation_data['hCodeValues'] in old_validation_data]
            old_input_validation = [old_validation['hCodeTokenIds'] for old_validation in old_validation_data]
            old_target_validation = [old_validation['hCodeValues'] for old_validation in old_validation_data]

            input_data.extend(old_input_validation)
            target_data.extend(old_target_validation)

        assert len(input_data) == len(target_data)

        correct = 0
        total = len(input_data)

        model.setup_for_prediction()


        for i in range(total):
            prediction = model.predict(input_data[i])
            if prediction == target_data[i]:
                correct += 1

        accuracy = correct / total * 100

        return accuracy, total


    # Trains latest deployed model until convergence with new training annotations
    def train_model(self, model: SHModel, input_training, target_training):

        model.setup_for_finetuning()

        mean_epoch_losses = []

        for epoch in range(self.epochs-1):
            losses = []
            for (input, target) in zip(input_training, target_training):
                loss = model.finetune_on(input, target)
                losses.append(loss)

            mean_loss = mean(losses)
            mean_epoch_losses.append(mean_loss)

            if epoch > 0 and mean_loss > mean_epoch_losses[epoch-1]:
                break

        return model

    # Loads latest model as json
    def load_latest_model_from_db(self, model_lang: str) -> SHModel:
        try: 
            if self.check_if_model_exists(model_lang):
                latest = self.get_latest_model_number(model_lang)
                return self.get_model_data_json(latest, model_lang)
            else:
                return None
        except:
            return None

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


    # Gets database object from DB
    def get_model_data_json(self, model_number: int, model_lang: str):
        try:
            json_data = {}

            db = self.client[self.database]
            collection = db[model_lang]

            document = collection.find({"modelNumber": model_number})
            
            for i in document:
                json_data = i

            return json_data
        except:
            return None

    # Gets pickled model
    def get_model_data_pickled(self, model_json) -> SHModel:

        if model_json and model_json['modelData']:
            pickled_model = model_json['modelData']
            return pickle.loads(pickled_model)
        else:
            return None

    # Removes duplicate tokenIds
    def remove_duplicates(self, train_a):
        filtered_a = []

        for a in train_a:
            if a['hCodeTokenIds'] not in filtered_a:
                filtered_a.append(a)

        return filtered_a



    def get_latest_model_number(self, model_lang: str):
        db = self.client[self.database]

        collection = db[model_lang]

        size = collection.count_documents({})

        return size

    # Make all instances of prediction.api pull latest model
    def deploy_latest_model(self, model_lang: str, model_number: int):
        try:
            for i in range(len(self.prediction_containers)):
                instance = i + 1
                url = f'http://syntax-highlighting-service-prediction-api-{instance}:8000/api/v1/deploy?lang={model_lang}&no={model_number}'
                
                requests.post(url)
                
        except Exception as e:
            logging.error(e)



    def load_training_annotations(self, lang):
        try:
            db = self.client[self.database]
            collection = db[self.collection]

            annotations_query = collection.aggregate([
                {
                    '$match': {'codeLanguage': lang, 'isTrained': False, 'isValidated': False}
                },

                {
                    "$sample": {'size': self.max_batch_size}
                },
            ])

            training = [a for a in annotations_query]

            return training


        except Exception as e:
            logging.error(e)
            return []

    def load_validation_annotations(self, lang):
        try:

            db = self.client[self.database]
            collection = db[self.collection]

            annotations_query = collection.aggregate([
                {
                    '$match': {'codeLanguage': lang, 'isTrained': False, 'isValidated': True}
                }
            ])

            validation = [a for a in annotations_query]

            return validation


        except Exception as e:
            logging.error(e)
            return []


    def save_model_to_db(self, model: SHModel, model_number: int, model_lang: str, training_size: int, validation_size: int, accuracy: float):
        try:
            pickled_model = pickle.dumps(model)

            db = self.client[self.database]
            collection = db[model_lang]

            query = collection.insert_one({"modelNumber": model_number, "modelData": pickled_model, "trainingSize": training_size, "validationSize": validation_size, "accuracy": accuracy, "createdAt": datetime.now().isoformat()})
        
            details = {'insertedId': query.inserted_id, "createdAt": datetime.now().isoformat()}

            return details
        except Exception as e: 
            logging.error(e)
            return 'Saving model to database failed'