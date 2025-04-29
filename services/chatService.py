import chat.models as chat_models
import doctor.models as doctor_models
from django.db.models import Q

class ChatService:
    def __init__(self,sender,reciever):
        self._recierver=reciever
        self._sender=sender
    def getChat(self):
        print(chat_models.DoctorChat.objects.filter(ChatRoom=self.getChatRoom()))
        return chat_models.DoctorChat.objects.filter(ChatRoom=self.getChatRoom())
    def sendChat(self,text):
        model=chat_models.DoctorChat()
        model.sender=doctor_models.DoctorModel.objects.get(pk=self._sender)
        model.reciever=doctor_models.DoctorModel.objects.get(pk=self._recierver)
        model.text=text
        model.save()
        return True
    
    def getChatRoom(self):
        firstTerminal=doctor_models.DoctorModel.objects.get(pk=self._sender)
        LastTerminal=doctor_models.DoctorModel.objects.get(pk=self._recierver)
        chatRoom=chat_models.DoctorChatRoom.objects.filter(Q(firstTerminal=firstTerminal ,secondTerminal=LastTerminal) | Q(firstTerminal=LastTerminal ,secondTerminal=firstTerminal)).first()
        if chatRoom: 
            return chatRoom 
        else:
            room=chat_models.DoctorChatRoom()
            room.firstTerminal=firstTerminal
            room.secondTerminal=LastTerminal
            room.save()
            return room
    