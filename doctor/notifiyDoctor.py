from .models import DoctorNotification,DoctorModel
def notifiyDoctor(sender, **kwargs):
    print(kwargs)
    if kwargs["created"]:
        notifiy=DoctorNotification()
        notifiy.doctor_id=DoctorModel.objects.get(pk=kwargs["instance"].doctor_id)
        notifiy.sender_id=kwargs["instance"].id
        notifiy.target_url="/doctor/patient/page/"+str(kwargs["instance"].id)
        notifiy.text="patient was recorded"
        notifiy.save()
