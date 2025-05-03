from patients.models import patient
from DataRepository.Repository import Repo
class patientsRepo(Repo):
    def mass_assignment(self, data:dict):
        patient_object=patient()
        patient_object.name=data["name"][0]
        patient_object.email=data["email"][0]
        patient_object.phone=data["phone"][0]
        patient_object.address=data["address"][0]
        patient_object.birth_date=data["birth_date"][0]
        patient_object.doctor=data["doctor"]
        patient_object.job=data["job"][0]
        patient_object.save()
        return patient_object
    def get_all(self):
        return patient.objects.all()
    def get_by_id(self, model_id):
        return patient.objects.get(pk=model_id)
    def delete(self, model_id):
        return patient.objects.filter(pk=model_id).delete()
    def update(self, model_id, **data):
        try:
            patient_object=patient.objects.get(pk=model_id)
            if data.get("name"):patient_object.name=data.get["name"]
            if data.get("email"):patient_object.email=data.get["email"]
            if data.get("phone"):patient_object.phone=data.get["phone"]
            if data.get("address"):patient_object.address=data.get("address")
            if data.get("job"):patient_object.job=data.get("job")
            return True
        except patient.DoesNotExist:
            return None
    def filter_patient_by_name(self,data):
        return patient.objects.filter(name__icontains=data["name"],doctor=data["doctor"])
    def count(self,data):
        return patient.objects.filter(doctor=data["doctor"]).count()