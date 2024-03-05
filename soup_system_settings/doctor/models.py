from django.db import models


# Классы менеджеров

class ActiveDoctorsManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active = True) 
    


class Departaments(models.Model): 
    name = models.CharField(max_length = 60, verbose_name = 'Имя') 
    
    def __str__(self) -> str:
        return f'{self.name}'


class Doctor(models.Model): 
    name = models.CharField(max_length = 60, verbose_name = 'Имя') 
    surname = models.CharField(max_length = 60, verbose_name = 'Фамилия')
    last_name =  models.CharField(max_length = 60, verbose_name = 'Отчество')
    departament = models.ForeignKey('Departaments', on_delete = models.PROTECT, related_name = 'doctors')
    is_active = models.BooleanField(default = True)
    objects = models.Manager()
    active = ActiveDoctorsManager()
    
    
    def __str__(self) -> str:
        return f'{self.surname} {self.name} {self.last_name} - {self.departament}'
    
    

    
    




    