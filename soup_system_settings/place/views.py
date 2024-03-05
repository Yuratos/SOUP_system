import re
from django.http import Http404, HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from django.views.decorators.cache import never_cache
from patient_queue.mongo_db import main_places, main_queue
from rest_framework.response import Response

# Create your views here.


@method_decorator(never_cache, name='dispatch')
class PlaceController(View):

    def get(self, request, place_name, doctor_info):
        pattern = r"^\w+\s\w+\s\w+\s-\s\w+$"
        
        if not re.match(pattern, doctor_info):
            raise Http404()
        
        fio = doctor_info.split('-')[0].strip()
        
        departament = doctor_info.split('-')[1].strip()

        need_queue = main_queue.find_one({'name': departament})
        
        check_doctor_mistake = need_queue.get('patients_in_cabinets')
        
        if place_name in check_doctor_mistake:
            check = need_queue.get('check')
            patient = check_doctor_mistake[place_name]
            patient['doctors'].insert(0, departament)
            print(patient)
            
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

