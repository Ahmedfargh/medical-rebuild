

from django.urls import re_path,path
from medical.consumer import DoctorIsOnLine
from chat.webSockets.chat.Consumer import DoctorChat as realTimeChat

websocket_urlpatterns = [
    re_path(r'ws/doctor/online$', DoctorIsOnLine.as_asgi()),
    path('ws/doctor/doctor/chat/<int:sender>/<int:reciever>/<int:roomid>/',realTimeChat.as_asgi()),
]
