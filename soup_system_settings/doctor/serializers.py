from rest_framework import serializers
from patient_queue.mongo_db import main_places
from . models import Doctor


class DoctorSerializer(serializers.Serializer):
    
    method = serializers.ChoiceField(['add', 'delete']) # проверяем, чтобы был передан метод 
    fio = serializers.CharField()
    departament = serializers.CharField()
    
    def validate(self, attrs):
        main_departaments = main_places.find_one({'name': 'main_departaments'}).get('all')
        departament = attrs.get('departament')
        fio = attrs.get('fio')
        method = attrs.get('method')
        fio = fio.split(' ')
        if departament not in main_departaments: 
             raise serializers.ValidationError({"departament":"Такого направления не существует"})
        if len(fio) != 3:
            raise serializers.ValidationError({"fio":"ФИО слишком короткое"})
        name = fio[1].strip()
        surname = fio[0].strip()
        last_name = fio[2].strip()
        if method == 'delete':
            try:
                Doctor.objects.get(surname=surname, name = name, last_name = last_name)
            except Exception:
                raise serializers.ValidationError({"fio":"Такого доктора нет в списке"})
        return attrs

