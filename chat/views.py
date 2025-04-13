from django.shortcuts import render
from doctor.models import DoctorModel
# Create your views here.
class ChatView:
    def getChatPage(request,pk=1,pk2=2):
        try:
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            return render(request,"chat content.html",{"doctor":doctor_obj})
        except DoctorModel.DoesNotExist:
            return render(request,"doctor/templates/login.html",{"status":0,"message":"session has ended"})
    def all_chats_page(request):
        try:
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            return render(request,"doctors chats.html",{"doctor":doctor_obj})
        except DoctorModel.DoesNotExist:
            return render(request,"doctor/templates/login.html",{"status":0,"message":"session has ended"})
    def search_doctor(request):
        try:
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            other_doctors_objects=DoctorModel.objects.filter(name__icontains=request.POST.get("name"))
            return render(request,"doctors chats.html",{"doctor":doctor_obj,"other_doctors":other_doctors_objects})
        except DoctorModel.DoesNotExist:
            return render(request,"doctor/templates/login.html",{"status":0,"message":"session has ended"})
