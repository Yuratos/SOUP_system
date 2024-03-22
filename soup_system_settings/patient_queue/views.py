from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import PatientSerializer
from .patient import Patient
from .mongo_db import main_queue, main_places


class RegisterPatientAPIView(APIView):
    
    parser_classes = [JSONParser]

    def post(self, request) -> Response:
        patient = PatientSerializer(data=request.data)
        data = request.data
        if patient.is_valid():
            surname = data.get('surname') 
            personal_id = data.get('personal_id') 
            departaments = data.get('departaments') 
            is_gold = data.get('is_gold') 
            patient_object = Patient.to_json(surname, personal_id, is_gold,  departaments)
            patient_departaments = patient_object.get('doctors')
            need_queue = patient_departaments[0]
            additional_departaments = main_places.find_one({'name': 'additional_departaments'}).get('all')
            if need_queue not in additional_departaments: 
                patient_object['return_to'] = need_queue
            patient_object['first_visit'] = True
            if (is_gold): 
                for i in range(3): 
                    if i != 2: 
                        patient_to_gold = 0
                    else: 
                        patient_to_gold =  patient_object  
                        
                    main_queue.update_one(
                        {"name": need_queue},  
                        {"$push": {"gold_queue": patient_to_gold}}, 
                        )
                return Response({'code': 200, 'status': 'ok'})
            
            if need_queue not in additional_departaments: 
                main_queue.update_one(
                            {"name": need_queue},  
                            {"$push": {"newbies_queue": patient_object}})       
            else: 
                main_queue.update_one(
                            {"name": need_queue},  
                            {"$push": {"participant_queue": patient_object}})       

            
            return Response({'code': 200, 'status': 'ok'})
        
        return Response({'status': '400', 'errors': patient.errors})

