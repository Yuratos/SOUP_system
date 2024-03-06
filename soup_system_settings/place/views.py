import re
from django.http import Http404
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import  render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from patient_queue.mongo_db import main_places, main_queue
from .places_info import additional_places

# Create your views here.


@method_decorator(never_cache, name='dispatch')
class PlaceController(View):

    def get(self, request, place_name, doctor_info):
        pattern = r"^\w+\s\w+\s\w+\s-\s\w+$"
        
        if not re.match(pattern, doctor_info) and doctor_info not in additional_places:
            raise Http404()
        
        doctor_info = doctor_info.split('-')
        
        if len(doctor_info) == 1: 
            fio = 'Идут сопутствующие процедуры'
            departament = doctor_info[0].strip()
        
        else:   
            fio = doctor_info[0].strip()
            departament = doctor_info[1].strip()

        need_queue = main_queue.find_one({'name': departament})
        
        check_doctor_mistake = need_queue.get('patients_in_cabinets')
        
        if place_name in check_doctor_mistake:
            check = need_queue.get('check')
            patient = check_doctor_mistake[place_name]
            patient['doctors'].insert(0, departament)

            main_queue.update_one(
                {"name": departament},
                {"$unset": {f"patients_in_cabinets.{place_name}": ""}}
                )
                

            if not check: 
                main_queue.update_one(
                    {"name": departament},  
                    {"$push": {"newbies_queue": {"$each": [patient], "$position": 0}}}
                )       
                
            else: 
                main_queue.update_one(
                    {"name": departament},  
                    {"$push": {"participant_queue": {"$each": [patient], "$position": 0}}}
                )  
                       
                          
        context = {'place_controller_number': place_name,
                   'doctor_fio': fio, 'doctor_departament': departament}
        
        
        return render(request, 'place/place_controller.html', context=context)


class PlaceScreen(View):
    def get(self, request, place_number):
        context = {'place_number': place_number}
        return render(request, 'place/place_screen.html', context=context)

