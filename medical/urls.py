"""
URL configuration for medical project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from doctor.views import DoctorView
from patients.views import PatientView
import patients.urls as url
from doctor.urls import symptomsUrl
from chat.url import chatUrl
urlpatterns = [
    path("admin/", admin.site.urls),
    path("doctor/login/page",DoctorView.logingPage,name="doctor_login"),
    path("doctor/sign/up",DoctorView.Register,name="doctor_register"),
    path("doctor/register",DoctorView.RegisterDoctor,name="register_operation"),
    path("doctor/login/dashboard",DoctorView.LoginDoctor,name="login_doctor"),
    path("doctor/dashbaord",DoctorView.Dashboard,name="doctor_dashboard"),
    path("patient/save",PatientView.add_patient,name="add_patient"),
    path("doctor/account",DoctorView.doctor,name="account"),
    path("doctor/modifiy/info",DoctorView.modifyAccount,name="mod_personal_info"),
    path("doctor/modifiy/personal_image",DoctorView.modifyPersonalImage,name="mod_personal_image"),
    path("doctor/modifiy/personal_certificate",DoctorView.modifyPersonalCertificate,name="mod_personal_certificate"),
    path("doctor/add/patient/note",DoctorView.saveNote,name="save_patient_note")

]
urlpatterns+=url.patient_url
urlpatterns+=symptomsUrl
urlpatterns+=chatUrl
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_URL)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
