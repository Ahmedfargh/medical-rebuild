import multiprocessing.process
from django.shortcuts import render
from .models import patient
from django.core.cache import cache
from django.http import JsonResponse
from patients.serializers import PatientSerializer
import rest_framework.decorators
import rest_framework.response
from django.core import serializers
from doctor.models import DoctorModel
from django.core.paginator import Paginator
from doctor.models import symptom
from patients.models import patient_suffer
from patients.models import patient
import threading
import time
from django.shortcuts import redirect
import datetime
from django.core.cache import cache
import pandas as pd
from medical import settings
import os
# Create your views here.
class PatientView:
    def add_patient(request):
        if request.method=="GET":
            pat=patient()
            pat.name=request.GET.get("name")
            pat.email=request.GET.get("email")
            pat.address=request.GET.get("address")
            pat.phone=request.GET.get("phone")
            pat.birth_date=request.GET.get("birth_date")
            pat.job=request.GET.get("job")
            pat.doctor=DoctorModel.objects.get(pk=request.session["doctor_id"])
            pat.save()
            return JsonResponse({"status":1,"patient":pat.to_json()})
    def search_patient(request):
        if request.method=="GET":
            key=request.GET["key"]
            patients=patient.objects.filter(name__icontains=key,doctor=request.session["doctor_id"])
            if patients.count():
                results=[]
                for pat in patients:
                    results.append(pat.to_json())
                return JsonResponse({"status":1,"results":results})
            return JsonResponse({"status":2,"message":"no records match"})
        return JsonResponse({"status":-1,"message":"no records match"})
    def patients_view(request):
        doctor=DoctorModel.objects.get(pk=request.session["doctor_id"])
        patients=patient.objects.filter(doctor=request.session["doctor_id"])
        paginator = Paginator(patients, 5)
        page_obj=None
        if request.GET.get("page"):
             page_obj = paginator.get_page(request.GET.get("page"))
        else:
             page_obj = paginator.get_page(1)
        return render(request,"patients.html",{"doctor":doctor,"patients":page_obj})
    def save_patient_update(request):
        print(request.GET)
        if request.method=="GET":
            patient_obj=patient.objects.get(pk=request.GET["id"])
            if patient_obj:
                patient_obj.name=request.GET["name"]
                patient_obj.job=request.GET["job"]
                patient_obj.address=request.GET["address"]
                patient_obj.email=request.GET["email"]
                patient_obj.birth_date=request.GET["birth_date"]
                patient_obj.save()
            return JsonResponse({"status":1,"message":"patient was updated"})
        return JsonResponse({"status":1,"message":"patient was updated"})
    def delete_patient(request):
        if request.method=="GET":
            try:
                patient.objects.get(pk=request.GET["patient_id"]).delete()
                return JsonResponse({"status":1,"message":"patient was deleted"})
            except patient.DoesNotExist:
                return JsonResponse({"status":0,"message":"patient was'nt found"})
    def record_suffer(request):
        if request.method=="GET":
            try:
                sym=symptom.objects.get(pk=request.GET["symptoms"])
                print(request.GET)
                for pat in dict(request.GET)["patients[0][]"]:
                    try:
                        patient_object=patient.objects.get(pk=int(pat))
                        suffer=patient_suffer()
                        suffer.patient_id=patient_object
                        suffer.symptom_id=sym
                        suffer.save()
                    except patient.DoesNotExist:
                        continue
                return JsonResponse({"status":1,"message":"patients symptoms recorded"})
            except symptom.DoesNotExist:
                return JsonResponse({"status":0,"message":'symptoms not found'})
    def load_patient(request):
        if request.method=="GET":
            try:
                doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
                symp=symptom.objects.filter(symptom_parent=None,doctor_id=doc)
                print(int(request.GET["patient"]))
                history=patient_suffer.objects.filter(patient_id=int(request.GET["patient"]))
                print(patient_suffer)
                return JsonResponse({"status":1,"history":patient_suffer.convert_to_json_list(history),"symptoms":symptom.convert_to_json_list(symp)})
            except DoctorModel.DoesNotExist:
                return JsonResponse({"status":0,"message":"account not found"})
            except symptom.DoesNotExist:
                return JsonResponse({"status":0,"message":"you don't have symptoms"})
            except patient_suffer.DoesNotExist:
                return JsonResponse({"status":0,"message":"patient does'nt have history"})
    def _get_name(request,symptom_name):
        for i in request.GET["symptoms"].split(","):
            try:
                symptom_obj=symptom.objects.get(pk=int(i))
                symptom_name.append(symptom_obj.name)
            except symptom.DoesNotExist:
                continue
    def record_diagnose(request):
        if request.method=="GET":
            try:
                doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
                symptom_name=[]
                processs=[
                    threading.Thread(target=PatientView._get_name,args=(request,symptom_name))
                ]
                for thread in processs:
                    thread.start()
                for thread in processs:
                    thread.join()
                suffer=patient_suffer()
                disease=symptom()
                disease.name=request.GET["disese"]
                disease.doctor_id=doc
                disease.save()
                suffer=patient_suffer()
                print(int(request.GET["patient_id"]))
                suffer.patient_id=patient.objects.get(pk=int(request.GET["patient_id"]))
                suffer.diagnosed_by=doc
                suffer.symptoms=symptom_name
                suffer.symptom_id=disease
                suffer.save()
                
                print(symptom_name)

                return JsonResponse({"status":1,"message":"diagnose_recorded"})
            except DoctorModel.DoesNotExist:
                return JsonResponse({"status":0,"message":"your account't was'nt found"})
        return JsonResponse({"status":0,"message":""})
    def patient_page(request,pk):
        try:
            print(pk)
            patient_obj=patient.objects.get(pk=pk)
            doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
            disease_history=patient_suffer.objects.filter(patient_id=patient_obj)
            paginator = Paginator(disease_history, 5)
            page_obj=None
            if request.GET.get("page"):
                page_obj = paginator.get_page(request.GET.get("page"))
            else:
                page_obj = paginator.get_page(1)
            notes_objects=patient_obj.getNotes()
            notes_paginate=Paginator(notes_objects,5)
            notes=None
            if request.GET.get("page"):
                notes = notes_paginate.get_page(request.GET.get("page"))
            else:
                notes = notes_paginate.get_page(1)
            cache.add(str(request.session["doctor_id"])+"_current_pagtient_history",page_obj.object_list.all(),600)
            print(cache.get(str(request.session["doctor_id"])+"_current_pagtient_history"))
            return render(request,"patient.html",{"doctor":doc,"patient":patient_obj,"history":page_obj,"notes":notes})
        except DoctorModel.DoesNotExist:
            return render(request,"login.html")
        except patient.DoesNotExist:
            return redirect("doctor_dashboard")
    def filter_patient_history(request,pk):
        try:
            patient_obj=patient.objects.get(pk=pk)
            doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
            from_date=request.POST.get("start_date")
            end_date=request.POST.get("end_date")
            from_date=datetime.datetime.strptime(from_date,'%Y-%m-%d')
            end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
            disease_history=patient_suffer.objects.filter(patient_id=patient_obj,created_at__range=(from_date,end_date))
            paginator = Paginator(disease_history, 5)
            page_obj=None
            if request.GET.get("page"):
                page_obj = paginator.get_page(request.GET.get("page"))
            else:
                page_obj = paginator.get_page(1)
            cache.add(str(request.session["doctor_id"])+"_current_pagtient_history",page_obj.object_list.all(),600)
            return render(request,"patient.html",{"doctor":doc,"patient":patient_obj,"history":page_obj})
        except DoctorModel.DoesNotExist:
            return render(request,"login.html")
        except patient.DoesNotExist:
            return redirect("doctor_dashboard")
    def load_patients_in_excel(request):
        try:
            doc=DoctorModel.objects.get(pk=request.session["doctor_id"])
            history=cache.get(str(request.session["doctor_id"])+"_current_pagtient_history")
            patient_obj=patient.objects.get(pk=int(request.POST.get("patitent_id")))
            data=patient_suffer.convert_to_json_list(history)
            symptoms=[]
            doctors=[]
            disease_name=[]
            created_at=[]
            for record in data:
                symptoms.append(record["symptoms"])
                doctors.append(record["doctor"]["name"])
                disease_name.append(record["symptom"]["name"])
                created_at.append(record["created_at"])
            df=pd.DataFrame(
                columns=["name","doctor","symptoms","created_at"],
                data={"name":disease_name,"doctor":doctors,"symptoms":symptoms,"created_at":created_at}
                            )
            print(os.getcwd())
            df.to_csv(os.getcwd()+"/media/patient/excel/"+str(patient_obj.id)+".csv")
            return render(request,"patient.html",{"doctor":doc,"patient":patient_obj,"history":history,"excel_file":"/media/patient/excel/"+str(patient_obj.id)+".csv"})
        except DoctorModel.DoesNotExist:
            return render(request,"login.html")
        except patient.DoesNotExist:
            return redirect("doctor_dashboard")
        