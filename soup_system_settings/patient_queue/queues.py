from collections import deque
from .patient import Patient

class GeneralQueue(): 
    
    def __init__(self) -> None:
        self.check_next_queue = 0 
        self._newbies_queue = deque() 
        self._participant_queue = deque() 
        self._patients_in_cabinets = {}
        
    
    def get_next_patient_number(self) -> str: 
        
        defacto_queue = self.check_queues_is_empty()
        
        if not defacto_queue: 
            return 0
        
        patient = defacto_queue.popleft()
        next_number = patient.personal_id 
        self.patients_in_cabinets[patient.personal_id] = patient
        self.check_next_queue += 1
        
        return next_number
    
    
    def end_patient_appointment(self, personal_id) -> Patient:
        patient = self.patients_in_cabinets[personal_id]
        del self.patients_in_cabinets[personal_id]
        return patient 
    
    
    def add_to(self, patient, queue_key):
        if queue_key == 1: 
            self.newbies_queue.append(patient)
        elif queue_key == 2: 
            self.participant_queue.append(patient)
            
            
    
    def check_queues_is_empty(self):
        
        if self.check_next_queue%2 == 0: 
            defacto_queue = self.newbies_queue
            previos_queue = self.participant_queue
            
        else: 
            defacto_queue = self.participant_queue
            previos_queue = self.newbies_queue
            
        if len(defacto_queue) == len(previos_queue) == 0: 
            return 0
            
        if len(defacto_queue) == 0 and len(previos_queue) != 0: 
            defacto_queue = previos_queue
                
        return defacto_queue
        
        
    @property 
    def newbies_queue(self): 
        return self._newbies_queue
    
    @property 
    def participant_queue(self): 
        return self._participant_queue
    
    @property 
    def patients_in_cabinets(self): 
        return self._patients_in_cabinets
    
    
class SurgeonQueue(GeneralQueue): 
    pass 
    
    