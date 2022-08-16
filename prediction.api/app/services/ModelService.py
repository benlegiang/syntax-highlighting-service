from datetime import datetime
import pickle
from app.services.MongoDatabase import MongoDatabase
from app.utils.SHModelUtils import JAVA_LANG_NAME, KOTLIN_LANG_NAME, PYTHON3_LANG_NAME, SHModel

database = 'syntaxHighlighting'

def check_if_model_exists(model_lang):

    try:
        client = MongoDatabase().client
        
        db = client[database]

        collection = db[model_lang]

        if collection.count_documents({}) > 0:
            return True
        else:
            return False
    except:
        print("Unable to establish database connection")

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


# Returns a model
def load_model_from_db(model_name, model_lang: str) -> SHModel:
    try:
        if check_if_model_exists(model_lang):
            print(f'Loading model for {model_lang} from database')
            json_data = {}

            client = MongoDatabase().client

            db = client[database]

            collection = db[model_lang]

            document = collection.find({"model_name": model_name})

            for i in document:
                json_data = i
            pickled_model = json_data['model_data']

            return pickle.loads(pickled_model)

        else:
            print(f'Initializing new model for {model_lang}')
            if model_lang == 'PYTHON3':
                python_model = SHModel(PYTHON3_LANG_NAME, 'model_latest')
                save_model_to_db('latest', python_model, model_lang)
                return python_model
            elif model_lang == 'JAVA':
                java_model = SHModel(JAVA_LANG_NAME, 'model_latest')
                save_model_to_db('latest', java_model, model_lang)
                return java_model
            elif model_lang == 'KOTLIN':
                kotlin_model = SHModel(KOTLIN_LANG_NAME, 'model_latest')
                save_model_to_db('latest', kotlin_model, model_lang)
                return kotlin_model

            return None

    except Exception as e: 
        print(e)
        return None

