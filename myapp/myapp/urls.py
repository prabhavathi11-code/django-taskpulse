"""
URL configuration for myapp project.
"""
from django.contrib import admin
from django.urls import path, include
from chatbot import views as chatbot_views
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("greet/", views.greet),
    path("", chatbot_views.chatbot_home, name="home"),
    path("chatbot/", include("chatbot.urls")),
]