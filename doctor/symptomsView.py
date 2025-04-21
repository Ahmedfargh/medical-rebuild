from django.shortcuts import render,redirect
from .models import DoctorModel
from .models import symptom
from django.http import JsonResponse
from patients.models import patient
from .models import symptom
from middlewares.LogedUserCache import freshCache
class symptoms:
    @freshCache
    def getView(request):
        try:
            doctor=DoctorModel.objects.get(pk=request.session["doctor_id"])
            symptoms=symptom.objects.filter(doctor_id=doctor)
            return render(request,"symptoms.html",{"doctor":doctor,"symptoms":symptoms})
        except DoctorModel.DoesNotExist:
            return render(request,"login.html",{"status":{"status":0,"message":"your account was deleted"}})
        except symptom.DoesNotExist:
            return render(request,"symptoms.html",{"doctor":doctor,"symptoms":[]})
    @freshCache
    def add_symptom(request):
        if request.method=="GET":
            sym=symptom()
            sym.name=request.GET["name"]
            sym.doctor_id=DoctorModel.objects.get(pk=request.session["doctor_id"])
            if request.GET.get("symptom_id"):
                try:
                    par_sym=symptom.objects.get(pk=request.GET.get("symptom_id"))
                    sym.symptom_parent=par_sym
                except symptom.DoesNotExist:
                    pass
            sym.save()
            return JsonResponse({"status":1,"message":"symptom is created"})
        return JsonResponse({"status":0,"message":"method not allowed"})
    @freshCache
    def diagnose_patient(request):
        try:
            doctor=DoctorModel.objects.get(pk=request.session["doctor_id"])
            doctor_patients=None
            sym=None
            try:
                doctor_patients=patient.objects.filter(doctor_id=request.session["doctor_id"])
                sym=symptom.objects.filter(doctor_id=request.session["doctor_id"])

            except patient.DoesNotExist:
                pass
            except symptom.DoesNotExist:
                pass
            print(doctor_patients)
            return render(request,"record_symptoms.html",{"doctor":doctor,"patients":doctor_patients,"syms":sym})            
        except DoctorModel.DoesNotExist:
            return render(request,"login.html",{"status":{"status":0,"message":"your account was deleted"}})
    @freshCache
    def diagnose_patients(request):
        if request.method=="GET":
            try:
                doctor=DoctorModel.objects.get(pk=request.session["doctor_id"])
                return render(request,"diagnose_patient.html",{"doctor":doctor})
            except DoctorModel.DoesNotExist:
                return render(request,"login.html")
    