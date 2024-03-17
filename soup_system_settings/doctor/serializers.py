from rest_framework import serializers
from patient_queue.departaments_objects import ALL_DEPARTAMENTS_NAME
from . models import Doctor


class DoctorSerializer(serializers.Serializer):

    method = serializers.ChoiceField(['add', 'delete']) # проверяем, чтобы был передан метод 
    fio = serializers.CharField()
    departament = serializers.ChoiceField(ALL_DEPARTAMENTS_NAME)

    def validate(self, attrs):
        fio = attrs.get('fio')
        method = attrs.get('method')
        fio = fio.split(' ')
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

