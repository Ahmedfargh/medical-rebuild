from django.urls import re_path
from medical.consumer import DoctorIsOnLine

websocket_urlpatterns = [
    re_path(r'ws/doctor/online$', DoctorIsOnLine.as_asgi()),
]
