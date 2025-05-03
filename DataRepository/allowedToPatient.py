from DataRepository.Repository import Repo
import patients.models as models
class allowTohandlePatientRepo(Repo):
    def __init__(self):
        pass
    def is_shared(patient,doctor):
        return models.allowedTo.objects.filter(doctor=doctor,patient=patient).count()>=1
    def mass_assignment(self, data):
        if data.get("object"):
            allowed= data.get("object")
            allowed.patient=data["patient"]
            allowed.doctor=data["doctor"]
            allowed.allowed=data["allowed"]
            return allowed
        