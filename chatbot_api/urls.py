# chatbot_api/urls.py
from django.urls import path
from .views import chatbot_api, test_api

urlpatterns = [
    path("chat/", chatbot_api, name="chat"),
    path("chit/", test_api, name="chit"),
]
