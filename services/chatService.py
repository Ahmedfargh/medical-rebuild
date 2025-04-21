import chat.models as chat_models
import doctor.models as doctor_models
from django.db.models import Q
class ChatService:
    def __init__(self,sender,reciever):
        self._recierver=reciever
        self._sender=sender
    def getChat(self):
        return chat_models.DoctorChat.objects.filter((Q(sender=self._sender) and Q(reciever=self._recierver)) or (Q(sender=self._recierver) and Q(reciever=self._sender)))
    def sendChat(self,text):
        model=chat_models.DoctorChat()
        model.sender=doctor_models.DoctorModel.objects.get(pk=self._sender)
        model.reciever=doctor_models.DoctorModel.objects.get(pk=self._recierver)
        model.text=text
        model.save()
        return True
    
        