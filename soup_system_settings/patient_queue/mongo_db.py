from pymongo import MongoClient

MONGO_HOST = '127.0.0.1'
MONGO_PORT = '27017'

mongo_client = MongoClient(host=MONGO_HOST ,
                      port=int('27017'),
                     )

db = mongo_client['soup_bd']
main_queue = db['queues']
main_places = db['places']