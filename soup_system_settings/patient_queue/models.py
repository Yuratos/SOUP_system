from django.db import models

# Create your models here. 
class Patient_Model(models.Model):  
    
    personal_id  = models.CharField(max_length = 10, verbose_name = 'Идентификатор', unique = True)
    
    surname = models.CharField(max_length = 60, verbose_name = 'Фамилия')
    
    is_gold = models.BooleanField()
    
    def __str__(self) -> str:
        return f'{self.personal_id} {self.surname}'
    
    class Meta: 
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Remote_From_Queue_PatientModel(models.Model):  
    
    personal_id  = models.CharField(max_length = 10, verbose_name = 'Идентификатор', unique = True)
    surname = models.CharField(max_length = 60, verbose_name = 'Фамилия')
    is_gold = models.BooleanField()
    
    def __str__(self) -> str:
        return f'{self.personal_id} {self.surname}'
    
    class Meta: 
        verbose_name = 'Удаленный из очереди пациент'
        verbose_name_plural = 'Удаленные из очереди пациенты'