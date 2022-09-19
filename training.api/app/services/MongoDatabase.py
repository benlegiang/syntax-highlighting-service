from pymongo import MongoClient

# mongo_uri = 'mongodb://admin:admin@localhost:27017'
mongo_uri = 'mongodb://admin:admin@mongodb:27017'

class MongoDatabase:
    class __MongoDatabase:
        def __init__(self):
            # Initialise mongo client
            self.client = MongoClient(mongo_uri)

    __instance = None

    def __init__(self):
        if not MongoDatabase.__instance:
            MongoDatabase.__instance = MongoDatabase.__MongoDatabase()

    def __getattr__(self, item):
        return getattr(self.__instance, item)