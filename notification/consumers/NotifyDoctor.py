from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.core.cache import cache
class DoctorNotifcation(AsyncWebsocketConsumer):
    connected_channels=set()

    async def connect(self):
        self.doctor_id=self.scope["url_route"]["kwargs"]["doctor_id"]
        self.group_name=f"doctor_{self.doctor_id}_group"
        print(self.group_name)
        DoctorNotifcation.connected_channels.add(self.group_name)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()
    async def disconnect(self, code):
        self.send(text_data=json.dumps({"text":"you are offline now"}))
        return await super().disconnect(code)
    async def receive(self, text_data=None, bytes_data=None):
        
        return 0
    async def notify_doctor(self,event):
        await self.send(text_data=json.dumps(event["payload"]))
    @classmethod
    def printConnected(cls):
        return list(cls.connected_channels)