from django.shortcuts import render,redirect
from django.http import JsonResponse,Http404

from doctor.forms import RegisterForm
from .models import DoctorModel
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,logout
from django.core.paginator import Paginator
from django.core.cache import cache

from patients.models import patient
from patients.models import patientNotes
from middlewares.OnlyPostRequests import OnlyPostRequest
from middlewares.DoctorObjectFound import OnlyAuthenticatedDoctor
from DataRepository.DoctorRepo import DoctorRepo
from middlewares.LogedUserCache import freshCache
from DataRepository.PatientsRepo import patientsRepo
from patients.models import allowedTo
from DataRepository.allowedToPatient import allowTohandlePatientRepo
# Create your views here.
class DoctorView:
    def logingPage(request):
        return render(request,"login.html")
    def Register(request):
        return render(request,"sign-up.html")
    @OnlyAuthenticatedDoctor
    def logOut(request):
        print(request.session)
        doctor_object=DoctorModel.objects.get(pk=request.session["doctor_id"])
        cache.delete("doctor_"+str(doctor_object.id)+"_is_loged")

        logout(request)
        del request.session
        return render(request,"login.html",{"status":{"status":1,"message":"your account was deleted"}})
    @OnlyPostRequest  
    def RegisterDoctor(request):
        if request.POST.get("password") and request.POST.get("password_confirm") and request.POST.get("password")==request.POST.get("password_confirm"):
            data=dict(request.POST)
            data["graduation_date"]=data["graduation_date"][0]
            data["certificate_file"]=request.FILES.get('certificate_file')
            data["perosnal_image"]=request.FILES.get('perosnal_image')
            repo=DoctorRepo()
            
            repo.mass_assignment(data)
            return render(request,"login.html",{"status":{"status":1,"message":"registeration success"}})
        return render(request,"register.html",{"status":{"status":0,"message":"in correct data"}})
    @OnlyPostRequest        
    def LoginDoctor(request):
        try:
            doctor=DoctorModel.objects.filter(email=request.POST.get("email")).get()
            if check_password(request.POST.get("password"),doctor.password):
                login(request,doctor)
                request.session["doctor_id"]=doctor.id
                cache.set("doctor_"+str(doctor.id)+"_is_loged",True,5)
                return redirect("doctor_dashboard")
            return render(request,"login.html",{"status":{"status":0,"message":"credentials are wrong"}})
        except  DoctorModel.DoesNotExist:

            return render(request,"login.html",{"status":{"status":0,"message":"credentials are wrong"}})
    @OnlyAuthenticatedDoctor
    @freshCache
    def Dashboard(request):
        doctor=DoctorModel.objects.get(pk=request.session["doctor_id"])
        patients=None
        try:
            patients=patient.objects.filter(doctor_id=doctor).order_by("-id")
        except patient.DoesNotExist:
            pass
        paginator = Paginator(patients, 5)
        page_obj=None
        if request.GET.get("page"):
            page_obj = paginator.get_page(request.GET.get("page"))
        else:
            page_obj = paginator.get_page(1)
        return render(request,"dashboard.html",{"doctor":doctor,"patients":page_obj})
    @OnlyAuthenticatedDoctor
    @freshCache
    def doctor(request):
        doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
        print(doc.to_json())
        return render(request,"account.html",{"doctor":doc})
    @OnlyPostRequest
    @OnlyAuthenticatedDoctor
    @freshCache
    def modifyAccount(request):
        print(request.POST)
        repo=DoctorRepo()
        repo.update(model_id=request.session["doctor_id"],data=dict(request.POST))
        return redirect("account")
    @OnlyPostRequest
    @OnlyAuthenticatedDoctor
    @freshCache
    def modifyPersonalImage(request):
        try:
            DoctorRepo().update(request.session["doctor_id"],{"personal_image":request.FILES["personal_image"]})
            return redirect("account")
        except Exception:
            raise
    @OnlyPostRequest
    @OnlyAuthenticatedDoctor
    @freshCache
    def modifyPersonalCertificate(request):
        try:
            DoctorRepo().update(request.session["doctor_id"],{"personal_certificate":request.FILES["personal_certificate"]})
            return redirect("account")
        except Exception:
            raise
    @OnlyAuthenticatedDoctor
    @freshCache
    def saveNote(request):
        try:
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            patient_obj=patient.objects.get(pk=request.GET["patient_id"])
            patientNotesObj=patientNotes()
            patientNotesObj.patient=patient_obj
            patientNotesObj.doctor=doctor_obj
            patientNotesObj.text=request.GET["text"]
            patientNotesObj.save()
            return JsonResponse({"status":1,"message":"the notes was saved"})
        except patient.DoesNotExist:
            return JsonResponse({"status":0,"message":"patient was'nt found"}) 
    @OnlyAuthenticatedDoctor
    @freshCache
    def getDoctorProfile(request,id):
        try:
            return JsonResponse(DoctorModel.objects.get(pk=id).to_json())
        except DoctorModel.DoesNotExist:
            return Http404("not found")
    @OnlyAuthenticatedDoctor
    @freshCache
    
    def sharePatient(request,doctor_id,patient_id):
        try:
            doctor_objs=DoctorRepo().get_by_id(doctor_id)
            patient_obj=patientsRepo().get_by_id(patient_id)
            if allowTohandlePatientRepo.is_shared(patient_obj,doctor_objs):
                return JsonResponse({"status":0,"message":"no duplicates allowed"})
            allowed=allowedTo()
            allowed.doctor=doctor_objs
            allowed.patient=patient_obj
            allowed.allowed=request.GET.get("permission")
            allowed.save()
            return JsonResponse({"patient":patient_obj.to_json(),"doctor":doctor_objs.to_json(),"status":1})
        except DoctorModel.DoesNotExist:
            return JsonResponse({"doctor":None,"patient":None,"status":0,"message":"doctor not found"})
        except patient.DoesNotExist:
            return JsonResponse({"doctor":None,"patient":None,"status":0,"message":"patient not found"})
