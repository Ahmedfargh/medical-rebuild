from django.db import models
from doctor.models import DoctorModel
import datetime
# Create your models here.

class DoctorChatRoom(models.Model):
    id=models.AutoField(primary_key=True)
    firstTerminal=models.ForeignKey(DoctorModel, on_delete=models.CASCADE,related_name="FirstTerminal")
    secondTerminal=models.ForeignKey(DoctorModel,on_delete=models.CASCADE,related_name="SecondTerminal")
    created_at=models.DateTimeField(default=datetime.datetime.now(),auto_now=False,auto_now_add=False)
    def convert_to_json(self):
        return {
            "id":self.id,
            "firstTerminal":self.firstTerminal,
            "sencondTerminal":self.secondTerminal,
            "datetime":self.created_at
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
class DoctorChat(models.Model):
    id=models.AutoField(primary_key=True)
    text=models.TextField()
    sender=models.ForeignKey(DoctorModel, on_delete=models.CASCADE,related_name="sender_object")
    reciever=models.ForeignKey(DoctorModel,on_delete=models.CASCADE,related_name="reciever")
    created_at=models.DateTimeField( default=datetime.datetime.now(),auto_now=False, auto_now_add=False)
    ChatRoom=models.ForeignKey(DoctorChatRoom, on_delete=models.CASCADE,related_name="Room",default=None)
    def convert_to_json(self):
        return {
            "id":self.id,
            "text":self.text,
            "sender":self.sender.to_json(),
            "reciever":self.reciever.to_json(),
            "datetime":self.created_at
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]