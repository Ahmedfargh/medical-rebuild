from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.core.cache import cache
class DoctorNotifcation(AsyncWebsocketConsumer):
    async def connect(self):
        self.doctor_id=self.scope["url_route"]["kwarg"]["doctor_id"]
        self.group_name=f"doctor_{self.doctor_id}_notification_channel"
        self.channel_name=f'{self.group_name}_channel'
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()
        self.send(text_data=json.dumps({"text":"you are online now "}))
    async def disconnect(self, code):
        self.send(text_data=json.dumps({"text":"you are offline now"}))
        return await super().disconnect(code)
    async def receive(self, text_data=None, bytes_data=None):
        
        pass
    async def notify_doctor(self,event):
        pass