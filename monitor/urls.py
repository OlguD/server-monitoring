from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('server_list/', views.server_list, name='server_list'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('settings/', views.settings, name='settings'),
]