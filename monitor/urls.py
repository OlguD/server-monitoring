from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard-data/', views.dashboard_data, name='dashboard_data'),
    path('servers/', views.server_list, name='server_list'),
    path('settings/', views.settings, name='settings'),
    path('add_server/', views.add_server, name='add_server'),
    path('save_settings/', views.save_settings, name='save_settings'),
]