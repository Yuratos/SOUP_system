from django.core.management.base import BaseCommand
from django.core.management import call_command
from patient_queue.mongo_db import main_places
from place.places_info import FREE_PLACES


class Command(BaseCommand):
    help = 'Заполняет MongoDB необходимыми значениями'

    def handle(self, *args, **kwargs):
        main_places.update_one({'name': 'free_places'}, {'$set': {'free': FREE_PLACES}})
        call_command('runserver')
