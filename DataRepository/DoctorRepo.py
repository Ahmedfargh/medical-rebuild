from doctor.models import DoctorModel
from DataRepository import Repository
from django.contrib.auth.hashers import make_password,check_password
from patients.models import patient,patientNotes
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
            raise 
    def filter(self,*args, **kwargs):
        pass
    def update(self,model_id,data:dict):
        print("data inside repo")
        print(data)
        doctor_object=DoctorModel.objects.get(pk=model_id)
        if "name" in data.keys():doctor_object.name=data["name"][0]
        if "address" in data.keys():doctor_object.address=data["address"][0]
        if "graduation_date" in data.keys():doctor_object.graduate_date=data["graduation_date"][0]
        if "phone" in data.keys():doctor_object.phone=data["phone"][0]
        if "email" in data.keys():doctor_object.email=data["email"][0]
        if "certificate_file" in data.keys():doctor_object.certificate_file=data.get("certificate_file")
        if "personal_image" in data.keys():
            doctor_object.personal_image=data.get("personal_image")
            print("shit")
        doctor_object.save()
    def delete(self,model_id):
        DoctorModel.objects.get(pk=model_id).delete()
        return True
    def getPatients(self,model_id):
        doctor=DoctorModel.objects.get(pk=model_id)
        patients=patient.objects.filter(doctor=doctor)
        return patients
    def getNotes(self,model_id):
        doctor=DoctorModel.objects.get(pk=model_id)
        return patientNotes.objects.filter(doctor=doctor)
    def search_doctor_by_name(self,name):
        return DoctorModel.objects.filter(name__icontains=name)
    def search_by_email(self,email):
        return DoctorModel.objects.filter(email__icontains=email)
    def search_by_address(self,address):
        return DoctorModel.objects.filter(email_icontains=address)
    