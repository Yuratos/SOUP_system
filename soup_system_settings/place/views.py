import re
from django.http import Http404
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import  render
from django.views import View
from django.utils.decorators import method_decorator
from django_lock import lock
from django.views.decorators.cache import never_cache
from doctor.models import Doctor
from patient_queue.mongo_db import  main_queue
from patient_queue.departaments_objects import ADDITIONAL_DEPARTAMENTS_NAME
from place.places_info import FREE_PLACES


@method_decorator(never_cache, name='dispatch')
class PlaceController(View):

    def get(self, request, place_name, doctor_info):
        pattern = r"^[\w-]+\s[\w-]+\s[\w-]+\s-\s[\w-]+(\s\w+)?$"
        
        if not re.match(pattern, doctor_info) and doctor_info not in ADDITIONAL_DEPARTAMENTS_NAME:
            raise Http404()
        

        doctor_info = doctor_info.split('-', 1)
           
        if len(doctor_info) == 1: 
            fio = 'Идут сопутствующие процедуры' 
            departament = doctor_info[0].strip()
        
        else:   
            fio = doctor_info[0].strip()
            departament = doctor_info[1].strip()

        need_queue = main_queue.find_one({'name': departament})
        
        check_doctor_mistake = need_queue.get('patients_in_cabinets')
        
        
        if place_name in check_doctor_mistake:
            patient = check_doctor_mistake[place_name]
            patient['doctors'].insert(0, departament)
            criteria = {'name': departament}
            check = need_queue.get('check')
            
            if patient.get('first_visit'): 
                name_queue = "newbies_queue"
                
            else: 
                name_queue = "participant_queue"
                
            
            check = not check  
            
            main_queue.update_one(
                {"name": departament},
                {"$unset": {f"patients_in_cabinets.{place_name}": ""}}
                )
            
            with lock(departament, timeout=2): 
                
                main_queue.update_one(
                    criteria,
                    {"$set": {"check": check}}
                )
                
                main_queue.update_one(
                    {"name": departament},  
                    {"$push": {name_queue: {"$each": [patient], "$position": 0}}}
                    )       
                
            
        context = {'place_controller_number': place_name,
                   'doctor_fio': fio, 'doctor_departament': departament}
        
        
        return render(request, 'place/place_controller.html', context=context)


class PlaceScreen(View):
    def get(self, request, place_number):
        context = {'place_number': place_number}
        return render(request, 'place/place_screen.html', context=context)
