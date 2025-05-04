from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
import datetime
from doctor.models import DoctorModel
from doctor.models import symptom
from django.db.models.signals import post_save
from doctor.notifiyDoctor import notifiyDoctor
from django.core.exceptions import ValidationError
# Create your models here.
def validate_size(value):
    file_size=value.size
    if file_size >20 * 1024 *1024:
        raise ValidationError("file must be less than 20 mb")
class patient(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.TextField()
    email=models.EmailField()
    password=models.TextField(null=True)
    address=models.TextField()
    phone=models.TextField()
    birth_date=models.DateField()
    Register_date=models.DateField(default=datetime.date.today)
    job=models.TextField()
    doctor=models.ForeignKey(DoctorModel, on_delete=models.CASCADE,null=True)
    def to_json(self):
        return {
            "name":self.name,
            "email":self.email,
            "address":self.address,
            "phone":self.phone,
            "birth_date":self.birth_date.__str__(),
            "job":self.job,
            "register_date":self.Register_date.__str__(),
            "id":self.id
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
    def getNotes(self):
        return patientNotes.objects.filter(patient=self)
class patient_suffer(models.Model):
    id=models.AutoField(primary_key=True)
    patient_id=models.ForeignKey(patient, on_delete=models.CASCADE)
    symptom_id=models.ForeignKey(symptom, on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=datetime.date.today)
    symptoms=models.JSONField(default=list)
    diagnosed_by=models.ForeignKey(DoctorModel, on_delete=models.SET_NULL,null=True)
    def to_json(self):
        return {
            "id":self.id,
            "patient":self.patient_id.to_json(),
            "symptom":self.symptom_id.to_json(),
            "symptoms":self.symptoms,
            "doctor":self.diagnosed_by.to_json() if self.diagnosed_by else None,
            "created_at":self.created_at if not self.created_at == None else " "
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
class patientNotes(models.Model):
    id=models.AutoField(primary_key=True)
    patient=models.ForeignKey(patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    text=models.TextField()
    created_at=models.DateField(default=datetime.date.today)
    def to_json(self):
        return {
            "id":self.id,
            "patient":self.patient.to_json(),
            "doctor":self.doctor.to_json(),
            "text":self.text,
            "creted_at":self.created_at
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
class allowedTo(models.Model):
    id=models.AutoField(primary_key=True)
    patient=models.ForeignKey(patient, on_delete=models.CASCADE)
    doctor=models.ForeignKey(DoctorModel ,on_delete=models.CASCADE)
    allowed=models.TextField(default="__read__")
    created_at=models.DateField(default=datetime.date.today, auto_now=False, auto_now_add=False)
    patient_approved=models.BooleanField(default=False)
    
    def to_json(self):
        return {
            "id":self.id,
            "patient":self.patient,
            "doctor":self.doctor,
            "created_at":self.created_at
        }
    
class patient_media(models.Model):
    id=models.AutoField(primary_key=True)
    patient=models.ForeignKey(patient, on_delete=models.CASCADE)
    file=models.FileField( upload_to="patient/media/",validators=[validate_size])
    created_at=models.DateField(default=datetime.date.today, auto_now=False, auto_now_add=False)
    file_type=models.TextField(default=None)
post_save.connect(notifiyDoctor,sender=patient)
