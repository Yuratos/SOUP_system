from pymongo import MongoClient

MONGO_HOST = 'mongodb'
MONGO_PORT = '27017'

mongo_client = MongoClient(host=MONGO_HOST ,
                      port=int(MONGO_PORT),
                     )

db = mongo_client['soup_bd']
main_queue = db['queues']
main_places = db['places']