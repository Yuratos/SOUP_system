from collections import deque

class Patient: 
    
    DEPARTAMENTS_WEIGHT = {'Хирургия': 1, 'Травматология': 2, 'МРТ': 3, 'Сдача крови': 4, 'Сдача мочи': 5}
       
    @classmethod
    def extend_doctors(cls, now_doctors, new_doctors): 
        now_doctors.extend(new_doctors)
        new_doctors =  list(sorted(now_doctors, key = lambda doctor: cls.DEPARTAMENTS_WEIGHT.get(doctor))) 
        return new_doctors
    
    @classmethod
    def to_json(cls, surname, personal_id, doctors): 
    
        return {'surname': surname, 'personal_id': personal_id, 'doctors': cls.extend_doctors([], doctors)}
    
        
        
        