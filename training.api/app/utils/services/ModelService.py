# Save model
import pickle
from datetime import datetime

from app.utils.SHModelUtils import SHModel
from app.utils.services.MongoDatabase import MongoDatabase

database = 'syntaxHighlighting'
annotations_collection = 'annotations'
batch_size = 1000
training_size = 0.8
test_size = 0.2

def save_model_to_db(model_name: str, model: SHModel, model_lang: str):
    client = MongoDatabase().client

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

    client = MongoDatabase().client

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

