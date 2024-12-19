from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('servers/', views.server_list, name='server_list'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('settings/', views.settings, name='settings'),
    path('add_server/', views.add_server, name='add_server'),
    path('save_settings/', views.save_settings, name='save_settings'),
]