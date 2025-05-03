from django.urls import path
from doctor.symptomsView import symptoms
from patients.views import PatientView
from .certificateViews import CertificateView
from doctor.views import DoctorView
symptomsUrl=[
    path("doctor/symptoms/page",symptoms.getView,name="symptomsBoard"),
    path("doctor/add/Symptoms",symptoms.add_symptom,name="add_symptoms"),
    path("doctor/symptoms/record",symptoms.diagnose_patient,name="record_symptoms"),
    path("doctor/patients/diagnose/disese",symptoms.diagnose_patients,name="diangose_disese"),
    path("doctor/certificate/index",CertificateView.index,name="certificateIndex"),
    path("doctor/add/certificate",CertificateView.add,name="upload_certificate"),
    path("doctor/get/doctor/profile/<int:id>/",DoctorView.getDoctorProfile),
    path("doctor/share/patient/<int:doctor_id>/<int:patient_id>/",DoctorView.sharePatient)

]