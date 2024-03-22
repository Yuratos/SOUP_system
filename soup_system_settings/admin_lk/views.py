from django.shortcuts import render
from django.views import View
from patient_queue.mongo_db import main_places


class AdminProfile(View): 
    def get(self, request): 
        additional_departaments = main_places.find_one({'name': "additional_departaments"}).get('all')
        main_departaments = main_places.find_one({'name': 'main_departaments'}).get('all')
        context = {'main_departaments': main_departaments, 'additional_departaments': additional_departaments}
        return render(request, 'admin_lk/admin_lk.html', context=context)