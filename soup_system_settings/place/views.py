import re
from django.http import Http404
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import  render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from patient_queue.mongo_db import main_places
from doctor.models import Doctor


@method_decorator(never_cache, name='dispatch')
class PlaceController(View):

    def get(self, request, place_name, doctor_info):
        free_places = main_places.find_one({'name': 'free_places'}).get('free')
        additional_departaments = main_places.find_one({'name': 'additional_departaments'}).get('all')
        all_doctors = [str(doctor) for doctor  in Doctor.active.all()]
        pattern = r"^[\w-]+\s[\w-]+\s[\w-]+\s-\s[\w-]+(\s\w+)?$"
        
        if not re.match(pattern, doctor_info) and doctor_info not in additional_departaments:
            raise Http404()
        
        if (doctor_info not in all_doctors and doctor_info not in additional_departaments) or place_name not in free_places: 
            raise Http404()
        
        doctor_info = doctor_info.split('-', 1)

        if len(doctor_info) == 1: 
            fio = 'Идут сопутствующие процедуры' 
            departament = doctor_info[0].strip()
        
        else:   
            fio = doctor_info[0].strip()
            departament = doctor_info[1].strip()

            
        context = {'place_controller_number': place_name,
                   'doctor_fio': fio, 'doctor_departament': departament, 'additional_departaments': additional_departaments}
        
        
        return render(request, 'place/place_controller.html', context=context)


class PlaceScreen(View):
    def get(self, request, place_number):
        all_free_places = main_places.find_one({'name': 'all_free_places'}).get('all')
        if place_number not in all_free_places: 
            raise Http404()
        context = {'place_number': place_number}
        return render(request, 'place/place_screen.html', context=context)
