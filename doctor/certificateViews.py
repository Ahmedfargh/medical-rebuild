from django.shortcuts import render,redirect
from .models import *
class CertificateView:
    def index(request):
        try:
            doctorObj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            certificates=certificate.objects.filter(doctor=doctorObj)
            return render(request,"certificate/index.html",{"doctor":doctorObj,"certificate":certificates})
        except DoctorModel.DoesNotExist:
            return render(request,"login.html",{"status":0,"message":"your session is ended"})
    def add(request):
        if request.method=="POST":
            try:
                doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
                cert=certificate()
                cert.name=request.POST.get("name")
                cert.file=request.FILES.get("certificate")
                cert.doctor=doctor_obj
                cert.save()
                return redirect("certificateIndex")
            except DoctorModel.DoesNotExist:
                return render(request,"login.html",{"status":0,"message":"your session is ended"})