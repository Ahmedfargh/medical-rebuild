from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.core.cache import cache
from chat.models import DoctorChat as ChatMessage
from chat.models import DoctorChatRoom
import doctor.models as DoctorsModels
from services.chatService import ChatService
class DoctorChat(AsyncWebsocketConsumer):

    async def connect(self):
        
        self.sender=self.scope["url_route"]["kwargs"]["sender"]
        self.reciever=self.scope["url_route"]["kwargs"]["reciever"]
        self.group_name=f'{self.reciever}_from_{self.sender}'
        self.roomId=self.scope["url_route"]["kwargs"]["roomid"]
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass
    @sync_to_async
    def save_chat(self,message):
        chat=ChatMessage()
        chat.text=message
        chat.sender=DoctorsModels.DoctorModel.objects.get(pk=self.sender)
        chat.reciever=DoctorsModels.DoctorModel.objects.get(pk=self.reciever)
        chat.ChatRoom=DoctorChatRoom.objects.get(pk=self.roomId)
        chat.save()

        ser=ChatService(self.sender,self.reciever)
        ser.getChat()
        return chat
    async def receive(self, text_data):
        
        data=json.loads(text_data)
        message=data["text"]
        print(message)
        await self.save_chat(message)
        await self.channel_layer.group_send(self.group_name,{
            'type':'broadcast.message',
            'message':message,
            
            
        })
        #return await self.channel_layer.group_send(self.group_name,{'type':'broadcast.message','message':message})
        return await self.send(text_data=json.dumps({"text":message}))
       
    async def broadcast_message(self,event):
        message=event["message"]
        sender_channel_name=event.get("sender_channel_name")
        await self.send(text_data=json.dumps({'message':message}))