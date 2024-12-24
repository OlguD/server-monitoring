from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect

from .utils.MonitorTools import MonitorTools

from monitor.Models.MonitorModels import (AllMonitorModel,
                 CPUModel, MemoryModel,
                 DiskModel, NetworkModel)
from monitor.models import ServerConfig

from user.models import User, UserConfig
from user.utils.is_user_subscribed import is_user_subscribed


@login_required(login_url='/user/login')
def add_server(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        server = ServerConfig(
            user=user,
            name=name,
            ip=ip,
            port=port,
            username=username,
            password=password,
            status=True
        )
        server.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/user/login')
def delete_server(request, server_id):
    if request.method == "DELETE":
        try:
            server = ServerConfig.objects.get(id=server_id)
            server.delete()
            return JsonResponse({"message": "Server deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": f"Error deleting server: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


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
@is_user_subscribed(time_limit=600) # 600 saniye (10 dakika)
@login_required(login_url='/user/login')
def dashboard(request, remaining_time=None):
    user = User.objects.filter(id=request.user.id).first()
    servers = ServerConfig.objects.filter(user=user)

    if remaining_time:
        minute_left = int(remaining_time//60)
        seconds_left = int(remaining_time%60)
        context = {"servers": servers, "remaining_time": remaining_time }
    else:
        context = {"servers": servers}
    return render(request, 'monitor/dashboard.html', context)


# @is_user_subscribed(time_limit=600) # 600 saniye (10 dakika)
@login_required(login_url='/user/login')
def dashboard_data(request):
    selected_server = request.GET.get('server')
    user = User.objects.filter(id=request.user.id).first()

    available_servers = ServerConfig.objects.filter(user=user)

    server = ServerConfig.objects.filter(
            user=user,
            name=selected_server
        ).first()

    try:
        monitor = MonitorTools(server)
        
        network_data = monitor.network_usage()
        all_monitor = AllMonitorModel(
            cpu=CPUModel(usage=monitor.cpu_usage()),
            memory=MemoryModel(usage=monitor.memory_usage()),
            disk=DiskModel(usage=monitor.disk_usage()),
            network=NetworkModel(
                total_usage_gb=network_data[0],
                sent_mb=network_data[1],
                recv_mb=network_data[2]
            ),
            processes=list(monitor.get_process_details())
        )
        
        data = {
            "server": server.name,
            "cpu": all_monitor.cpu.model_dump(),
            "memory": all_monitor.memory.model_dump(),
            "disk": all_monitor.disk.model_dump(),
            "network": all_monitor.network.model_dump(),
            'processes': [process.model_dump() for process in all_monitor.processes]
        }
        return JsonResponse(data)
            
    except Exception as e:
        return JsonResponse({
            "error": f"Server connection error: {str(e)}",
            "server_info": {
                "name": server.name,
                "ip": server.ip,
                "port": server.port
            }
        }, status=500)

    except Exception as e:
        return JsonResponse({
            "error": f"General error: {str(e)}"
        }, status=500)

@login_required(login_url='/user/login')
def server_list(request):
    user = User.objects.filter(id=request.user.id).first()
    servers = ServerConfig.objects.filter(user=user)
    context = {"servers": servers}
    return render(request, 'monitor/server_list.html', context)

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

def subscription_page(request):
    return render(request, 'user/subscription_page.html')
