from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_home, name='chatbot_home'),
    path('api/send/', views.api_send_message, name='api_send'),
    path('api/conversations/', views.api_get_conversations, name='api_conversations'),
    path('api/conversations/<uuid:conv_id>/messages/', views.api_get_messages, name='api_messages'),
    path('api/conversations/<uuid:conv_id>/delete/', views.api_delete_conversation, name='api_delete'),
    path('api/clear-all/', views.api_clear_all, name='api_clear_all'),
]
