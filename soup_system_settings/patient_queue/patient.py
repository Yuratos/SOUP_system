from .mongo_db import main_places

class Patient: 
       
    @classmethod
    def extend_doctors(cls, now_doctors, new_doctors): 
        DEPARTAMENTS_WEIGHT = main_places.find_one({'name': 'departaments_weight'}).get('all')
        now_doctors.extend(new_doctors)
        new_doctors =  list(sorted(now_doctors, key = lambda doctor: DEPARTAMENTS_WEIGHT.get(doctor), reverse=True)) 
        print(2000)
        return new_doctors
    
    @classmethod
    def to_json(cls, surname, personal_id, is_gold, doctors): 
        return {'surname': surname, 'personal_id': personal_id, 'is_gold': is_gold, 'doctors': cls.extend_doctors([], doctors)}
    
        
        