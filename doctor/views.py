from django.shortcuts import render,redirect
from django.http import JsonResponse

from doctor.forms import RegisterForm
from .models import DoctorModel
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,logout
from django.core.paginator import Paginator

from patients.models import patient
from patients.models import patientNotes
# Create your views here.
class DoctorView:
    def logingPage(request):
        return render(request,"login.html")
    def Register(request):
        return render(request,"sign-up.html")
    def logOut(request):
        try:
            doctor_object=DoctorModel.objects.get(pk=request.session["doctor_id"])
            logout(request)
            del request.session
        except DoctorModel.DoesNotExist:
            return render(request,"login.html",{"status":{"status":1,"message":"your account was deleted"}})
        return render(request,"login.html",{"status":{"status":1,"message":"you loged out"}})
    def RegisterDoctor(request):
        if request.method =="POST":
            if request.POST.get("password") and request.POST.get("password_confirm") and request.POST.get("password")==request.POST.get("password_confirm"):

                doctor=DoctorModel()
                doctor.name=request.POST.get("name")
                doctor.email=request.POST.get("email")
                doctor.address=request.POST.get("address")
                doctor.phone=request.POST.get("phone")
                doctor.graduate_date=request.POST.get("graduation_date")
                doctor.password=make_password(request.POST.get("password"))
                uploaded_certificate = request.FILES.get('certificate_file')
                uploaded_image = request.FILES.get('perosnal_image')
                doctor.certificate_file=uploaded_certificate
                doctor.personal_image=uploaded_image
                doctor.save()
                return render(request,"login.html",{"status":{"status":1,"message":"registeration success"},"doctor":doctor})
            return render(request,"register.html",{"status":{"status":0,"message":"in correct data"}})
        return render(request,"register.html")        
    def LoginDoctor(request):
        if request.method=="POST":
            print(request.POST.get("email"))
            try:
                doctor=DoctorModel.objects.filter(email=request.POST.get("email")).get()
                if check_password(request.POST.get("password"),doctor.password):
                    login(request,doctor)
                    request.session["doctor_id"]=doctor.id
                    return redirect("doctor_dashboard")
                return render(request,"login.html",{"status":{"status":0,"message":"credentials are wrong"}})
            except  DoctorModel.DoesNotExist:

                return render(request,"login.html",{"status":{"status":0,"message":"credentials are wrong"}})
        return render(request,"login.html",{"status":{"status":0,"message":"credentials are wrong"}})
    def Dashboard(request):
        try:
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
        except DoctorModel.DoesNotExist:
            return render(request,"login.html",{"status":{"status":0,"message":"your account was deleted"}})
    def doctor(request):
        try:
            doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
            print(doc.to_json())
            return render(request,"account.html",{"doctor":doc})
        except DoctorModel.DoesNotExist:
            return render(request,"login.html",{"status":{"status":0,"message":"your account was deleted"}})
    def modifyAccount(request):
        if request.method=="POST":
            try:
                doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
                doctor_obj.name=request.POST.get("name")
                doctor_obj.email=request.POST.get("email")
                doctor_obj.phone=request.POST.get("phone")
                doctor_obj.address=request.POST.get("address")
                doctor_obj.save()
                return redirect("account")
            except DoctorModel.DoesNotExist:
                return render(request,"login.html",{"status":{"status":0,"message":"your account was deleted"}})
    def modifyPersonalImage(request):
        if request.method=="POST":
            try:
                doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
                doctor_obj.personal_image=request.FILES['personal_image']
                doctor_obj.save()
                return redirect("account")
            except DoctorModel.DoesNotExist:
                return render(request,"login.html",{"status":{"status":0,"message":"your account was deleted"}})
            except Exception:
                raise
    def modifyPersonalCertificate(request):
        if request.method=="POST":
            try:
                doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
                doctor_obj.certificate_file=request.FILES["personal_certificate"]
                doctor_obj.save()
                return redirect("account")
            except DoctorModel.DoesNotExist:
                return render(request,"login.html",{"status":0,"message":"your account was deleted"})
            except Exception:
                raise
    def saveNote(request):
        if request.method=="GET":
            try:
                doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
                patient_obj=patient.objects.get(pk=request.GET["patient_id"])
                patientNotesObj=patientNotes()
                patientNotesObj.patient=patient_obj
                patientNotesObj.doctor=doctor_obj
                patientNotesObj.text=request.GET["text"]
                patientNotesObj.save()
                return JsonResponse({"status":1,"message":"the notes was saved"})
            except DoctorModel.DoesNotExist:
                return JsonResponse({"status":0,"message":"session ended"})
            except patient.DoesNotExist:
                return JsonResponse({"status":0,"message":"patient was'nt found"}) 
