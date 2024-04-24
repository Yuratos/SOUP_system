from rest_framework import serializers
from .models import PatientModel
from patient_queue.departaments_objects import ALL_DEPARTAMENTS_NAME, ADDITIONAL_DEPARTAMENTS_NAME

class PatientSerializer(serializers.ModelSerializer):
    
    departaments = serializers.ListField(child = serializers.ChoiceField(ALL_DEPARTAMENTS_NAME + ADDITIONAL_DEPARTAMENTS_NAME), allow_empty=False) 
     
    class Meta: 
        model = PatientModel
        fields = '__all__' 
        
    def save(self, **kwargs):
        validated_data = self.validated_data 
        validated_data.pop('departaments', None)
        return super().save(**kwargs)
    
    