from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PatientSerializer
from .mongo_db import main_queue
from rest_framework.parsers import JSONParser
from .patient import Patient




class RegisterPatientAPIView(APIView):
    
    parser_classes = [JSONParser]

    def post(self, request) -> Response:
        patient = PatientSerializer(data=request.data)
        if patient.is_valid():
            patient.save()
            surname = request.data.get('surname') 
            personal_id = request.data.get('personal_id') 
            departaments = request.data.get('departaments') 
            patient_object = Patient.to_json(surname, personal_id, departaments)
            patient_departaments = patient_object.get('doctors')
            need_queue = patient_departaments[0]
            main_queue.update_one(
                        {"name": need_queue},  
                        {"$push": {"newbies_queue": patient_object}})           
            return Response({'code': 200, 'status': 'ok'})
        
        return Response({'status': '400', 'errors': patient.errors})

