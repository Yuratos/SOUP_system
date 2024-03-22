from rest_framework import serializers
from patient_queue.mongo_db import main_places

class PatientSerializer(serializers.Serializer):
    personal_id  = serializers.CharField(max_length = 10)  
    surname = serializers.CharField(max_length = 60)
    is_gold = serializers.BooleanField()
    departaments = serializers.ListField(allow_empty=False)
    
    def validate(self, attrs):
        additional_departaments = main_places.find_one({'name': 'additional_departaments'}).get('all')
        main_departaments = main_places.find_one({'name': 'main_departaments'}).get('all')
        all_departaments = main_departaments + additional_departaments
        departaments = attrs.get('departaments')
        for departament in departaments: 
            if departament not in all_departaments: 
                raise serializers.ValidationError({"departaments":"Одного из выбранных направлений не существует"})
        return super().validate(attrs) 
     
    