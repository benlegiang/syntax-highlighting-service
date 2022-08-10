# Save model
from pymongo import MongoClient
import pickle
from datetime import datetime

from app.utils.SHModelUtils import SHModel

mongo_uri = 'mongodb://admin:admin@localhost:27017'
# mongo_uri = MongoClient('mongodb://admin:admin@mongodb:27017')
database = 'syntaxHighlighting'
annotations_collection = 'annotations'
batch_size = 1000
training_size = 0.8
test_size = 0.2

def save_model_to_db(model_name: str, model: SHModel, model_lang: str):
    client = MongoClient(mongo_uri)

    model.persist_model()
    try:
        pickled_model = pickle.dumps(model)

        db = client[database]
        collection = db[model_lang]

        query = collection.insert_one({"model_name": model_name, "model_data": pickled_model, "created_at": datetime.now().isoformat()})
    
        details = {'inserted_id': query.inserted_id, "created_at": datetime.now().isoformat()}

        return details
    except Exception as e: 
        print(e)
        return 'Saving model to database failed'

def load_annotations_from_db(code_lang):

    client = MongoClient(mongo_uri)

    try:
        db = client[database]
        collection = db[annotations_collection]

        query_result = collection.aggregate([

            {
                '$match': {'codeLanguage': code_lang}
            },

            {
                "$sample": {'size': batch_size}
            },
            
        ])


        return 0


    except Exception as e:
        print(e)
        return 'Loading annotations from database failed'

def fine_tune_model():

    pass

