import patients
import doctor
class Counter:
    def __init__(self, doctor_object):
        self.doctor_obj=doctor_object
    def countPatient(self):
        return patients.models.patient.objects.filter(doctor=self.doctor_obj).count()
    def countCertificate(self,status=False):
        return doctor.models.certificate.objects.filter(doctor=self.doctor_obj,status=status).count()