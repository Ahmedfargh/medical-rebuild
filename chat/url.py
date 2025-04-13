"""
"""
from django.urls import path
from .views import ChatView
chatUrl=[
    path("doctor/chats/doctors",ChatView.all_chats_page,name="doctors_chats"),
    path("doctors/chat/P<pk>\d+/P<pk2>\d+",ChatView.getChatPage,name="chat_page_doctors"),
    path("doctors/search/",ChatView.search_doctor,name="search_doctor")
]