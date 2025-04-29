from django.shortcuts import render
from doctor.models import DoctorModel
from django.db.models import Q
from chat.models import DoctorChat
from services.chatService import ChatService 
from middlewares.DoctorObjectFound import OnlyAuthenticatedDoctor
from middlewares.LogedUserCache import freshCache
from middlewares.onlyGetRequests import OnlyGetRequest
from services.chatService import ChatService
from django.http import JsonResponse
from middlewares.OnlyPostRequests import OnlyPostRequest
# Create your views here.
class ChatView:
    @OnlyAuthenticatedDoctor
    @OnlyGetRequest
    @freshCache
    def getChatPage(request,pk=1,pk2=2):
        try:
            service=ChatService(pk,pk2)
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            reciever=DoctorModel.objects.get(pk=pk2)
            room=service.getChatRoom()
            print("Test")
            print(room)
            chat_content=service.getChat()
            return render(request,"chat content.html",{"doctor":doctor_obj,"chat_content":chat_content,"reciever":reciever,"room":room})
        except DoctorModel.DoesNotExist:
            return render(request,"doctor/templates/login.html",{"status":0,"message":"session has ended"})
    @OnlyAuthenticatedDoctor
    @OnlyGetRequest
    @freshCache
    def all_chats_page(request):
        try:
            
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            return render(request,"doctors chats.html",{"doctor":doctor_obj})
        except DoctorModel.DoesNotExist:
            return render(request,"doctor/templates/login.html",{"status":0,"message":"session has ended"})
    @OnlyAuthenticatedDoctor
    @OnlyPostRequest
    @freshCache
    def search_doctor(request):
        try:
            
            doctor_obj=DoctorModel.objects.get(pk=request.session["doctor_id"])
            other_doctors_objects=DoctorModel.objects.filter(name__icontains=request.POST.get("name"))
            if request.POST.get("name")=="":
                return render(request,"doctors chats.html",{"doctor":doctor_obj,"other_doctors":None})
            return render(request,"doctors chats.html",{"doctor":doctor_obj,"other_doctors":other_doctors_objects})
        except DoctorModel.DoesNotExist:
            return render(request,"doctor/templates/login.html",{"status":0,"message":"session has ended"})
    