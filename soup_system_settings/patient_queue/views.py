from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import PatientSerializer
from .mongo_db import main_queue
from .patient import Patient
from .models import Patient_Model
from .departaments_objects import ADDITIONAL_DEPARTAMENTS_NAME


class RegisterPatientAPIView(APIView):
    
    parser_classes = [JSONParser]

    def post(self, request) -> Response:
        patient = PatientSerializer(data=request.data)
        data = request.data
        if patient.is_valid():
            patient.save()
            surname = data.get('surname') 
            personal_id = data.get('personal_id') 
            departaments = data.get('departaments') 
            is_gold = data.get('is_gold') 
            patient_object = Patient.to_json(surname, personal_id, is_gold,  departaments)
            patient_departaments = patient_object.get('doctors')
            need_queue = patient_departaments[0]
            if need_queue not in ADDITIONAL_DEPARTAMENTS_NAME: 
                patient_object['return_to'] = need_queue
            patient_object['first_visit'] = True
            if (is_gold): 
                main_queue.update_one(
                    {"name": need_queue},  
                    {"$push": {"newbies_queue": {"$each": [patient_object], "$position": 2}}}
                    )
                return Response({'code': 200, 'status': 'ok'})
            
            if need_queue not in ADDITIONAL_DEPARTAMENTS_NAME: 
                main_queue.update_one(
                            {"name": need_queue},  
                            {"$push": {"newbies_queue": patient_object}})       
            else: 
                main_queue.update_one(
                            {"name": need_queue},  
                            {"$push": {"participant_queue": patient_object}})       

            
            return Response({'code': 200, 'status': 'ok'})
        
        return Response({'status': '400', 'errors': patient.errors})

