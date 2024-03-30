import pymongo
from core.constant.base_mongodb import Request


class MongoConnection(object):
    def __init__(self):
        self.mongo_client = None
        self.db_name = None

    def init_connection(self, db_name):
        self.db_name = db_name
        self.mongo_client = pymongo.MongoClient(Request.CONNECT_URL + db_name)

    def connect_db(self):
        return self.mongo_client[self.db_name]

    def upsert(self, collection_name, condition=None, documents=None):
        db_connection = self.connect_db()[collection_name]
        # db_connection.update_one({ '_id' : 'stats'}, { '$set': data1 }, upsert=True)
        data = db_connection.find_one({} if not condition else condition)
        if not data:
            db_connection.insert_one(documents)
        else:
            db_connection.update_one(condition, {'$set': documents}, upsert=True)

    def get_all(self, collection_name, condition=None):
        db_connection = self.connect_db()[collection_name]
        # db_connection.update_one({ '_id' : 'stats'}, { '$set': data1 }, upsert=True)
        data = db_connection.find({} if not condition else condition)
        return data

    def get_one(self, collection_name, condition=None):
        db_connection = self.connect_db()[collection_name]
        # db_connection.update_one({ '_id' : 'stats'}, { '$set': data1 }, upsert=True)
        data = db_connection.find_one({} if not condition else condition)
        return data


# a = MongoConnection()
# a.init_connection("facebook")
# a.upsert("users", documents={"user_id": 1000})
