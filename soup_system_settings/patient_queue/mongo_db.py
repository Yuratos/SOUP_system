from pymongo import MongoClient

# mongo_client = MongoClient('mongodb://mongoadmin:secret@mongodb:27017/')
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['soup_bd']
main_queue = db['queues']
main_places = db['places'] 

