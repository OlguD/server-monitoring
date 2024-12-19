from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from monitor.Models.MonitorModels import (AllMonitorModel,
                 CPUModel, MemoryModel,
                 DiskModel, NetworkModel)
from monitor.Models.ServerConfig import ServerConfig
from user.models import User, UserConfig
from .utils.MonitorTools import MonitorTools

@login_required(login_url='/user/login')
def add_server(request):
    if request.method == "POST":
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        server = ServerConfig(
            name=name,
            ip=ip,
            port=port,
            username=username,
            password=password,
            status='active'
        )
        server.save()

@login_required(login_url='/user/login')
def save_settings(request):
   if request.method == "POST":
       try:
           user = User.objects.filter(email=request.user.email).first()
           if not user:
               user = User.objects.create(
                   username=request.user.username,
                   email=request.user.email,
                   id=request.user.id
               )
           user_config = UserConfig.objects.get_or_create(user=user)[0]

           user_config.email_notifications_enabled = request.POST.get('email_notifications_enabled') == 'true'
           user_config.check_interval = request.POST.get('check_interval')
           user_config.response_timeout = request.POST.get('response_timeout')
           user_config.log_retention_days = request.POST.get('log_retention_days')
           user_config.save()

           return redirect('settings')
       except Exception as e:
           print(f"Error in save_settings: {e}")
           return redirect('settings')
   
   return redirect('settings')


# Create your views here.
@login_required(login_url='/user/login')
def dashboard(request):
    # AllMonitorModel doğrudan render'a gönderilemez
    # Dictionary'ye dönüştürülmeli veya context oluşturulmalı

    network_data = MonitorTools.network_usage()

    all_monitor = AllMonitorModel(
        cpu=CPUModel(usage=MonitorTools.cpu_usage()),
        memory=MemoryModel(usage=MonitorTools.memory_usage()),
        disk=DiskModel(usage=MonitorTools.disk_usage()),
        network=NetworkModel(
            total_usage_gb=network_data[0],
            sent_mb=network_data[1],
            recv_mb=network_data[2]
        ),
        processes=list(MonitorTools.get_process_details())
    )
    
    # Pydantic modelini dictionary'ye çevir
    context = {
        'cpu': all_monitor.cpu.model_dump(),
        'memory': all_monitor.memory.model_dump(),
        'disk': all_monitor.disk.model_dump(),
        'network': all_monitor.network.model_dump(),
        'processes': [process.model_dump() for process in all_monitor.processes]
    }
    
    return render(request, 'monitor/dashboard.html', context)

@login_required(login_url='/user/login')
def server_list(request):
    return render(request, 'monitor/server_list.html')

@login_required(login_url='/user/login')
def monitoring(request):
    return render(request, 'monitor/monitoring.html')

@login_required(login_url='/user/login')
def settings(request):
   try:
       user = User.objects.filter(email=request.user.email).first()
       if not user:
           user = User.objects.create(
               username=request.user.username, 
               email=request.user.email,
               id=request.user.id
           )
       user_config = UserConfig.objects.get_or_create(user=user)[0]
       context = {"user_config": user_config}
       return render(request, 'monitor/settings.html', context)
   except Exception as e:
       print(f"Error in settings view: {e}")
       return redirect('dashboard')