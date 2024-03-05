import pickle
from .queues import GeneralQueue, SurgeonQueue
from django.core.cache import cache

QUEUES = {'Общая': GeneralQueue(), 'Хирургия': SurgeonQueue()}

cache.set('QUEUES', pickle.dumps(QUEUES))