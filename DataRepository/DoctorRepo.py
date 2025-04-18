from doctor.models import DoctorModel
from DataRepository import Repository
from django.contrib.auth.hashers import make_password,check_password

class DoctorRepo(Repository.Repo):
    def mass_assignment(self,data:dict):
        doctor=DoctorModel()
        doctor.name=data["name"][0]
        doctor.address=data["address"][0]
        doctor.certificate_file=data["certificate_file"]
        doctor.personal_image=data["perosnal_image"]
        doctor.password=make_password(data["password"][0])
        doctor.graduate_date=data["graduation_date"]
        doctor.phone=data["phone"][0]
        doctor.email=data["email"][0]
        doctor.save()
        return True
    def get_all(self):
        return DoctorModel.objects.all()
    def get_by_id(self,model_id:int):
        try:
            return DoctorModel.objects.get(pk=model_id)
        except DoctorModel.DoesNotExist:
            return None
    def filter(self,*args, **kwargs):
        pass
    def update(self,model_id,data:dict):
        doctor_object=DoctorModel.objects.get(pk=data["doctor_id"])
        if data.get("name"):doctor_object.name=data["name"]
        if data.get("address"):doctor_object.address=data["address"]
        if data.get("graduation_date"):doctor_object.graduate_date=data["graduation_date"]
        if data.get("phone"):doctor_object.phone=data["phone"]
        if data.get("email"):doctor_object.email=data["email"]
        if data.get("certificate_file"):doctor_object.certificate_file=data.get("certificate_file")
        if data.get("perosnal_image"):doctor_object.personal_image.data.get("personal_image")
        doctor_object.save()
    def delete(self,model_id):
        DoctorModel.objects.get(pk=model_id).delete()
        return True