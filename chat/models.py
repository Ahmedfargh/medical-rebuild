from django.db import models
from doctor.models import DoctorModel
import datetime
# Create your models here.
class DoctorChat(models.Model):
    id=models.AutoField(primary_key=True)
    text=models.TextField()
    sender=models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    reciever=models.ForeignKey(DoctorModel,on_delete=models.CASCADE)
    created_at=models.DateTimeField( default=datetime.datetime.now(),auto_now=False, auto_now_add=False)
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