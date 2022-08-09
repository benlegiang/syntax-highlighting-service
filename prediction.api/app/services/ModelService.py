import pickle
from pymongo import MongoClient

from app.utils.SHModelUtils import SHModel


# mongo_uri = 'mongodb://admin:admin@localhost:27017'
mongo_uri = 'mongodb://admin:admin@mongodb:27017'

database = 'syntaxHighlighting'

# Returns a model
def load_model_from_db(model_name, model_lang: str) -> SHModel:
    try:
        json_data = {}

        client = MongoClient(mongo_uri)

        db = client[database]

        collection = db[model_lang]

        document = collection.find({"model_name": model_name})

        for i in document:
            json_data = i
        pickled_model = json_data['model_data']

        return pickle.loads(pickled_model)

    except Exception as e: 
        print(e)
        return None