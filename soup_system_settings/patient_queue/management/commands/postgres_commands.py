from django.core.management.base import BaseCommand
from doctor.models import Departaments
from patient_queue.mongo_db import mongo_client
from patient_queue.departaments_objects import ALL_DEPARTAMENTS_NAME


class Command(BaseCommand):
    help = 'Заполняет MongoDB необходимыми значениями'

    def handle(self, *args, **kwargs):
        try:
            for name in ALL_DEPARTAMENTS_NAME: 
                departament = Departaments.objects.create(name = name)
                departament.save()
                
            print('--Записи успешно занесены в БД--')
        
        except Exception as err: 
            print('--Возникла ошибка--')
            print(err)