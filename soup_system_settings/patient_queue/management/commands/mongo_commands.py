from django.core.management.base import BaseCommand
from patient_queue.mongo_db import mongo_client
from patient_queue.departaments_objects import ALL_DEPARTAMENTS_NAME, ADDITIONAL_DEPARTAMENTS_NAME, DEPARTAMENTS_WEIGHT
from place.places_info import FREE_PLACES


class Command(BaseCommand):
    help = 'Заполняет MongoDB необходимыми значениями'

    def handle(self, *args, **kwargs):
        try:
            free_places = {'name': 'free_places', 'free': []}
            all_free_places = {'name': 'all_free_places', 'all':  FREE_PLACES + ADDITIONAL_DEPARTAMENTS_NAME}
            main_departaments =  {'name': 'main_departaments', 'all':  ALL_DEPARTAMENTS_NAME}
            additional_departaments = {'name': 'additional_departaments', 'all':  ADDITIONAL_DEPARTAMENTS_NAME}
            departaments_weight = {'name': 'departaments_weight', 'all': DEPARTAMENTS_WEIGHT}
            db = mongo_client['soup_bd']
            collection_queue = db['queues']
            collection_places = db['places']
            collection_places.insert_many([free_places, all_free_places, main_departaments, additional_departaments, departaments_weight])
            for name in ALL_DEPARTAMENTS_NAME + ADDITIONAL_DEPARTAMENTS_NAME:
                pattern = {'name': name, 'check': 0, 'newbies_queue': [],
                        'participant_queue': [], 'gold_queue': [], 'patients_in_cabinets': {}}
                collection_queue.insert_one(pattern)
            print('--Записи успешно занесены в БД--')
        
        except Exception as err: 
            print('--Возникла ошибка--')
            print(err)

