from django.shortcuts import render
from django.views import View
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .models import Doctor, Departaments
from .serializers import DoctorSerializer
from patient_queue.mongo_db import main_places



class HelloDoctorPage(View): 
    def get(self, request): 
        return render(request, 'doctor/hello_doctor.html')
    
    
class GetMainDepartaments(APIView):
    def get(self, request): 
         main_departaments = main_places.find_one({'name': "main_departaments"}).get('free')
         return Response({"main_departaments": main_departaments})
    

class GetAdditionalDepartaments(APIView):
    def get(self, request): 
         additional_departaments = main_places.find_one({'name': "additional_departaments"}).get('free')
         return Response({"main_departaments": additional_departaments})


class GetFreePlacesAPI(APIView):
    def get(self, request): 
        free_palces = main_places.find_one({'name': "free_places"}).get('free')
        if not request.GET.get('search'): 
            return Response({"places": free_palces})
        search_item = request.GET.get('search') 
        free_palces = [place for place in free_palces if search_item.lower() in place.lower()]
        return Response({"places": free_palces})
    
    
    
class GetAllPlacesAPI(APIView): 
    def get(self, request): 
        all_free_palces = main_places.find_one({'name': "all_free_places"}).get('free')
        return Response({'places': all_free_palces})
    

class GetDoctorsAPI(APIView):
    def get(self, request):
        additional_departaments = main_places.find_one({'name': 'additional_departaments'}).get('all')
        if not request.GET.get('search'): 
            doctors = Doctor.active.all()
            doctors_list = [str(doctor) for doctor in doctors]
            doctors_list.extend(additional_departaments)
            return Response({"doctors": doctors_list})
        search_letters = request.GET.get('search').capitalize()
        doctors = Doctor.active.filter(Q(name__icontains = search_letters) | Q(surname__icontains = search_letters) | Q(last_name__icontains = search_letters) | Q(departament__name__icontains = search_letters))
        addititional = [str(name) for name in additional_departaments if search_letters.lower() in name.lower()]
        doctors_list = [str(doctor) for doctor in doctors]
        doctors_list.extend(addititional)
        return Response({"doctors" : doctors_list})


class RemoveAddDoctorAPI(APIView): 
    
    parser_classes = [JSONParser]
    
    def patch(self, request): 
        data = request.data
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid(): 
            fio = data.get('fio').split(' ')
            surname = fio[0].strip()
            name = fio[1].strip()
            last_name = fio[2].strip()
            departament = data.get('departament').strip()
            if data.get('method') == 'delete': 
                try:
                    departament_obj = Departaments.objects.get(name = departament)
                    doctor = Doctor.objects.get(surname = surname, name = name, last_name = last_name, departament = departament_obj)
                    doctor.delete()
                    return Response({'status': '200'})
                except Exception: 
                    return Response({'status': '400', 'errors': serializer.errors})
            else:
                try:
                    departament_obj = Departaments.objects.get(name = departament)
                    doctor = Doctor.objects.create(surname = surname, name = name, last_name = last_name, departament = departament_obj)
                    doctor.save()
                    return Response({'status': '200'})
                except Exception:
                    return Response({'status': '400', 'errors': serializer.errors})
                
        else: 
            return Response({'status': '400', 'errors': serializer.errors})
        


