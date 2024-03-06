import json
import requests
import asyncio
from django_lock import lock
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from patient_queue.mongo_db import main_places, main_queue
from patient_queue.patient import Patient



class PlaceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.place_name = self.scope['url_route']['kwargs']['place_name']
        self.palce_group_name = 'place_%s' % self.place_name
        query_string = self.scope['query_string'].decode()
        
        await asyncio.sleep(0.6)
        
        if query_string == 'open':
            criteria = {'name': 'free_places'}
            update = {'$pull': {'free': self.place_name}}
            result = main_places.find_one_and_update(criteria, update)

        await self.channel_layer.group_add(
            self.palce_group_name,
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
            self.palce_group_name,
            self.channel_name
        )
        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json.get('close'):
            await self.channel_layer.group_send(
                self.palce_group_name,
                {
                    'type': 'close_controller',
                }
            )
            return
        
        departament = text_data_json['departament']
        place = text_data_json['place']
        fio = text_data_json.get('fio')
        patient_departaments = text_data_json.get('end_patient')
        
        if patient_departaments:
            patient_departaments = text_data_json.get('end_patient')
            with lock(departament, timeout=2):
                need_queue = main_queue.find_one({'name': departament})
                cabinets_patients = need_queue.get('patients_in_cabinets')
                patient = cabinets_patients[place] 
                
                new_doctors = Patient.extend_doctors(patient.get('doctors'), patient_departaments)  
                patient['doctors'] = new_doctors
                main_queue.update_one(
                        {"name": new_doctors[0]},  
                        {"$push": {"participant_queue": patient}})     
                
                main_queue.update_one(
                        {"name": departament},
                        {"$unset": {f"patients_in_cabinets.{place}": ""}}
                        )      
            return 
                
                
        criteria = {'name': departament}

        with lock(departament, timeout=2):
            need_queue = main_queue.find_one({"name": departament})
            check = need_queue['check']

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

                await self.channel_layer.group_send (
                    self.palce_group_name,
                    {
                        'type': 'next_number',
                        'departament': departament,
                        'place': place,
                        'fio': fio,
                        'next_number': 0

                    }
                )
                return

            if len(defacto_queue) == 0:
                defacto_queue = none_defacto_queue
                defacto_name = none_defacto_name

            next_number = defacto_queue[0]['personal_id']
            pop_doctor = defacto_queue[0]['doctors'].pop(0)
            patient = defacto_queue[0]

            updates = {

                # Удаление первого элемента из newbies_queue
                "$pop": {f"{defacto_name}": -1}

            }

            main_queue.update_one(criteria, updates)

            updates = {

                # Запись нового объекта по указанному ключу
                "$set": {f"patients_in_cabinets.{self.place_name}": patient}
            }

            main_queue.update_one(criteria, updates)
            
        
        await self.channel_layer.group_send(
            self.palce_group_name,
            {
                'type': 'next_number',
                'departament': departament,
                'place': place,
                'fio': fio,
                'next_number':  next_number
            }
        )

    async def close_controller(self, event):
        await self.send(text_data=json.dumps({
            'close': '1'
        }))
        

    async def next_number(self, event):
        place = event['place']
        departament = event['departament']
        fio = event['fio']
        next_number = event['next_number']
        
        
        await self.send(text_data=json.dumps({
            'fio': fio,
            'next_number': next_number,
            'departament': departament
        }))

