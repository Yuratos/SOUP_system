from django.core.management.base import BaseCommand
from patient_queue.mongo_db import mongo_client
from patient_queue.departaments_objects import ALL_DEPARTAMENTS_NAME, ADDITIONAL_DEPARTAMENTS_NAME


class Command(BaseCommand):
    help = 'Заполняет MongoDB необходимыми значениями'

    def handle(self, *args, **kwargs):
        try:
            free_places = {'name': 'free_places', 'free': []}
            db = mongo_client['soup_bd']
            collection_queue = db['queues']
            collection_places = db['places']
            collection_places.insert_one(free_places)
            for name in ALL_DEPARTAMENTS_NAME + ADDITIONAL_DEPARTAMENTS_NAME:
                pattern = {'name': name, 'check': 0, 'newbies_queue': [],
                        'participant_queue': [], 'gold_queue': [], 'patients_in_cabinets': {}}
                collection_queue.insert_one(pattern)
            print('--Записи успешно занесены в БД--')
        
        except Exception as err: 
            print('--Возникла ошибка--')
            print(err)

