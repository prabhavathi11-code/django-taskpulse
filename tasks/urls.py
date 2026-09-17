from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('tasks/create/', views.task_create, name='create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='delete'),
    path('tasks/<int:pk>/toggle/', views.task_toggle, name='toggle'),
    path('health/', views.health_check, name='health'),
]
