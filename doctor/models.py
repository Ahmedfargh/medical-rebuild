from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError
import datetime
# Create your models here.
def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")

def validate_image(file):
    if not file.content_type.startswith('image/'):
        raise ValidationError("Only image files are allowed.")

class DoctorModel(AbstractBaseUser):
    id=models.AutoField(primary_key=True)
    name=models.TextField()
    email=models.EmailField( max_length=32,unique=True)
    address=models.TextField()
    password=models.TextField()
    phone=models.TextField()

    graduate_date=models.DateField()
    certificate_file=models.FileField( upload_to="doctor/file/certificated", validators=[validate_pdf])
    personal_image=models.ImageField( upload_to="doctor/file/perosnal_image",validators=[validate_image])
    gender=models.CharField(default="male",max_length=10)
    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "address":self.address,
            "phone":self.phone,
            "graduate_date":self.graduate_date,
            "gender":self.gender
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
    def getNotifications(self):
        return DoctorNotification.objects.filter(doctor_id=self)
class DoctorNotification(models.Model):
    id=models.AutoField(primary_key=True)
    text=models.TextField()
    doctor_id=models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    target_url=models.URLField(null=True, max_length=200)
    sender_id=models.IntegerField(null=True)
    model=models.CharField(default="doctor", max_length=50)
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
    
class symptom(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField( max_length=50)
    doctor_id=models.ForeignKey(DoctorModel,  on_delete=models.CASCADE)
    symptom_parent=models.ForeignKey('self',  on_delete=models.CASCADE,null=True)
    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "doctor":self.doctor_id.to_json(),
            "symptom_parent":self.symptom_parent.to_json() if self.symptom_parent else None
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]
class certificate(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.TextField()
    doctor=models.ForeignKey(DoctorModel, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    file=models.FileField(upload_to="doctor/certificated",validators=[validate_pdf],default=True)
    certified_at=models.DateField(default=datetime.date.today)
    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "doctor":self.doctor.to_json(),
            "status":self.status
        }
    def convert_to_json_list(query):
        return [model.to_json() for model in query]