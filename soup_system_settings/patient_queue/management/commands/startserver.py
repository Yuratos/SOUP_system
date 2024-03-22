from django.core.management.base import BaseCommand
from django.core.management import call_command
from patient_queue.mongo_db import main_places



class Command(BaseCommand):
    help = 'Заполняет MongoDB необходимыми значениями'

    def handle(self, *args, **kwargs):
        all_free_places = main_places.find_one({'name': 'all_free_places'}).get('all')
        main_places.update_one({'name': 'free_places'}, {'$set': {'free': all_free_places}})        
        #call_command('runserver')


