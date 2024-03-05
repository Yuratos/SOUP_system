from django.shortcuts import render
from django.views import View
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from place.places_info import FREE_PLACES
from patient_queue.mongo_db import main_places
from .models import Doctor
# Create your views here.

class HelloDoctorPage(View): 
    def get(self, request): 
        return render(request, 'doctor/hello_doctor.html')
    

class GetFreePlacesAPI(APIView):
    def get(self, request): 
        free_palces = main_places.find_one({'name': "free_places"}).get('free')
        if not request.GET.get('search'): 
            return Response({"places": free_palces})
        search_item = request.GET.get('search') 
        free_palces = [place for place in free_palces if search_item in place]
        return Response({"places": free_palces})
    

class GetDoctorsAPI(APIView):
    def get(self, request):
        if not request.GET.get('search'): 
            doctors = Doctor.active.all()
            doctors_list = [str(doctor) for doctor in doctors]
            return Response({"doctors": doctors_list})
        search_letters = request.GET.get('search').capitalize()
        doctors = Doctor.active.filter(Q(name__icontains = search_letters) | Q(surname__icontains = search_letters) | Q(last_name__icontains = search_letters) | Q(departament__name__icontains = search_letters))
        doctors_list = [str(doctor) for doctor in doctors]
        return Response({"doctors" : doctors_list})


