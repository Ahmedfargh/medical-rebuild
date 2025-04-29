from channels.generic.websocket import AsyncWebsocketConsumer
import json
import doctor
from asgiref.sync import sync_to_async
from django.core.cache import cache

class DoctorIsOnLine(AsyncWebsocketConsumer):
    onlineDoctor=set()
    async def connect(self):
        await self.accept()
        

    async def disconnect(self, close_code):
        pass

    @sync_to_async
    def getDoctorObjects(self,id):
        return doctor.models.DoctorModel.objects.get(is_online=True,pk=id)
    @sync_to_async
    def is_authenticated(self,object):
        return cache.has_key("doctor_"+str(object)+"_is_loged")
    
    async def receive(self, text_data):
        
        data=json.loads(text_data)
        doctorId=data["doctor_id"]
        add_online=data["add_to_online_user"]
        # try:
        #     doctor_object=await self.getDoctorObjects(doctorId)
        #     print(await self.is_authenticated(doctor_object))
        #     return await self.send(text_data=json.dumps({
        #         'message':await self.is_authenticated(doctor_object)
        #     }))
        # except doctor.models.DoctorModel.DoesNotExist:
        #     await self.send(text_data=json.dumps({
        #         'message':"doctor objects not found"
        #     }))
        if add_online:
            
            return await self.send(text_data=json.dumps({"is_online":True}))
        return await self.send(text_data=json.dumps({"is_online":await self.is_authenticated(doctorId),"doctor_id":doctorId}))
       
        