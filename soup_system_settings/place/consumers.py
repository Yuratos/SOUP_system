import json
import asyncio
from django_lock import lock
from channels.generic.websocket import AsyncWebsocketConsumer
from patient_queue.mongo_db import main_places, main_queue
from patient_queue.patient import Patient
from patient_queue.models import PatientModel, RemoteFromQueuePatientModel
from .translate import translation_dict




# Полезные функции

def del_patient_from_queue(personal_id, surname, is_gold): 
    try: 
        print(personal_id, surname, is_gold)
        PatientModel.objects.delete(personal_id = personal_id, surname = surname, is_gold = is_gold)
        RemoteFromQueuePatientModel.objects.create(personal_id = personal_id, surname = surname, is_gold = is_gold)
    
    except Exception as error: 
        print(error)


def send_patient_to_queue(patient, next_doctor, main_queue): 
    
      if patient.get('is_gold'): 
          main_queue.update_one(
            {"name": next_doctor},  
            {"$push": {"participant_queue": {"$each": [patient], "$position": 2}}}
            )
                        
      else:     
          main_queue.update_one(
            {"name": next_doctor},
            {"$push": {"participant_queue": patient}}
            )
                        
    
# Точнка входа в веб-сокет

class PlaceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.place_name = self.scope['url_route']['kwargs']['place_name']
        self.translate_place_name = ''.join([translation_dict.get(letter) if not letter.isdigit() else letter for letter in self.scope['url_route']['kwargs']['place_name'].lower().replace(' ', '')])
        self.place_group_name = 'place_%s' % self.translate_place_name
        query_string = self.scope['query_string'].decode()

        await asyncio.sleep(0.6)

        if query_string == 'open':
            criteria = {'name': 'free_places'}
            update = {'$pull': {'free': self.place_name}}
            result = main_places.find_one_and_update(criteria, update)

        await self.channel_layer.group_add(
            self.place_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        if close_code == 1001:
            return

        criteria = {'name': 'free_places'}
        update = {'$push': {'free': self.place_name}}

        main_places.find_one_and_update(criteria, update)

        await self.channel_layer.group_discard(
            self.place_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json.get('close'):
            await self.channel_layer.group_send(
                self.place_group_name,
                {
                    'type': 'close_controller',
                }
            )
            return

        if text_data_json.get('break'):
            await self.channel_layer.group_send(
                self.place_group_name,
                {
                    'type': 'break_controller',
                }
            )
            return

        departament = text_data_json['departament']
        place = text_data_json['place']
        fio = text_data_json.get('fio')

        patient_departaments = text_data_json.get('end_patient')
        
        # Когда получаем от сокета информацию о окончании приема пациента
        if patient_departaments:
            need_queue = main_queue.find_one({'name': departament})
            cabinets_patients = need_queue.get('patients_in_cabinets')
            patient = cabinets_patients.get(place)
            next_doctors = patient.get('doctors')
    
            if patient.get('first_visit'): 
                del patient['first_visit']
            
                        
            if patient_departaments == 'nothing':
                print('step_1')
                print(next_doctors)
                
                if len(next_doctors) == 0 and not patient.get('return_to'): 
                    print('step_2')
                    del_patient_from_queue(patient.get('personal_id'), patient.get('surname'), patient.get('is_gold'))
                    next_doctor = 'Отсутствует'
                    print('step_2')

                
                elif len(next_doctors) == 0 and patient.get('return_to'): 
                    next_doctor = patient.get('return_to')
                    next_doctors.append(next_doctor)
                    try:
                        del patient['return_to']
                    except Exception as err: 
                        pass 
                    
                    
                else: 
                    next_doctor = next_doctors[0]
                    # send_patient_to_queue(patient, next_doctor, main_queue)
                    
                    
                
            else: 
                if 'no_return' in patient_departaments: # Если врач отметил, что пациента возвращать не нужно
                    try:
                        del patient_departaments[patient_departaments.index('no_return')]
                        del patient['return_to']
                    except Exception as err: 
                            pass 
                
                # Удаление пациента, если никаких врачей не передано и пациента не нужно возвращать
                if len(patient_departaments) == len(next_doctors) == 0:
                    del_patient_from_queue(patient.get('personal_id'), patient.get('surname'), patient.get('is_gold'))
                    next_doctor = 'Отсутствует'
                
                else:
                    new_doctors = Patient.extend_doctors(next_doctors, patient_departaments)
                    next_doctor = new_doctors[0]
                    patient['doctors'] = new_doctors
                    
                
            await self.channel_layer.group_send(
                self.place_group_name,
                {
                        'type': 'next_doctor',
                        'next_doctor': next_doctor
                }
            )
                
            main_queue.update_one(
                {"name": departament},
                {"$unset": {f"patients_in_cabinets.{place}": ""}}
            )
            
            with lock(departament, timeout=2):
                send_patient_to_queue(patient, next_doctor, main_queue)
                
            return

        criteria = {'name': departament}
        need_queue = main_queue.find_one({"name": departament})
        check = need_queue.get('check')

        with lock(departament, timeout=2): 
            main_queue.update_one(
                criteria,
                {"$set": {"check": not check}}
            )

            if not int(check):
                defacto_queue = need_queue['newbies_queue']
                none_defacto_queue = need_queue['participant_queue']
                defacto_name = 'newbies_queue'
                none_defacto_name = 'participant_queue'

            else:
                defacto_queue = need_queue['participant_queue']
                none_defacto_queue = need_queue['newbies_queue']
                defacto_name = 'participant_queue'
                none_defacto_name = 'newbies_queue'

            if len(defacto_queue) == len(none_defacto_queue) == 0:

                await self.channel_layer.group_send(
                    self.place_group_name,
                    {
                        'type': 'next_number',
                        'departament': departament,
                        'place': place,
                        'fio': fio,
                        'next_number': 0,
                        'first_in': 0
                    }
                )
                return

            if len(defacto_queue) == 0:
                defacto_queue = none_defacto_queue
                defacto_name = none_defacto_name

            if defacto_name == 'newbies_queue':
                first_in = 1
            else:
                first_in = 0

            next_number = defacto_queue[0]['personal_id']
            pop_doctor = defacto_queue[0]['doctors'].pop(0)
            patient = defacto_queue[0]

            updates = {
                # Удаление первого элемента из очереди
                "$pop": {f"{defacto_name}": -1}
            }

            main_queue.update_one(criteria, updates)

            updates = {

                # Запись нового объекта по указанному ключу
                "$set": {f"patients_in_cabinets.{self.place_name}": patient}
            }

            main_queue.update_one(criteria, updates)

        await self.channel_layer.group_send(
            self.place_group_name,
            {
                'type': 'next_number',
                'departament': departament,
                'place': place,
                'fio': fio,
                'next_number':  next_number,
                'first_in': first_in
            }
        )

    async def close_controller(self, event):
        await self.send(text_data=json.dumps({
            'close': '1'
        }))

    async def break_controller(self, event):
        await self.send(text_data=json.dumps({
            'break': '1'
        }))

    async def next_doctor(self, event):
        next_doctor = event['next_doctor']
        await self.send(text_data=json.dumps({
            'next_doctor': next_doctor
        }))

    async def next_number(self, event):
        place = event['place']
        departament = event['departament']
        fio = event['fio']
        next_number = event['next_number']
        first_in = event['first_in']

        await self.send(text_data=json.dumps({
            'fio': fio,
            'next_number': next_number,
            'departament': departament,
            'first_in': first_in
        }))
