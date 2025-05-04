from django.urls import path
from .views import PatientView
patient_url=[
    path("doctor/patient/search",PatientView.search_patient,name="search_patient"),
    path("doctor/patients",PatientView.patients_view,name="patients_page"),
    path("doctor/patients/update",PatientView.save_patient_update,name="update_patient"),
    path("doctor/patients/delete",PatientView.delete_patient,name="delele_patient"),
    path("doctor/patients/record/symptoms",PatientView.record_suffer,name="record_Symptoms_api"),
    path("doctor/patient/load/patients",PatientView.load_patient,name="load_patients"),
    path("doctor/patient/recorddiagnose/",PatientView.record_diagnose,name="record_diangose"),
    path("doctor/patient/page/?P<pk>\d+",PatientView.patient_page,name="patient_page"),
    path("doctor/patient/history/?P<pk>\d+/filter",PatientView.filter_patient_history,name="filter_patient_history"),
    path("doctor/patient/excel",PatientView.load_patients_in_excel,name="load_patient_into_excel"),
    path("doctor/patient/upload/media",PatientView.uploadPatientMedia,name="upload_patient_media")
]