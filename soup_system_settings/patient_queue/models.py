from django.db import models

# Create your models here. 
class Patient(models.Model):  
    
    personal_id  = models.IntegerField(verbose_name = 'Идентификатор')
    
    surname = models.CharField(max_length = 60, verbose_name = 'Фамилия')
    
    def __str__(self) -> str:
        return f'{self.personal_id} {self.surname}'
    
    class Meta: 
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
