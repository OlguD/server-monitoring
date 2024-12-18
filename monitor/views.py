from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from monitor.Models.MonitorModels import AllMonitorModel, CPUModel, MemoryModel, DiskModel, NetworkModel
from .utils.MonitorTools import MonitorTools

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

@login_required
def server_list(request):
    return render(request, 'monitor/server_list.html')

@login_required
def monitoring(request):
    return render(request, 'monitor/monitoring.html')

@login_required
def settings(request):
    return render(request, 'monitor/settings.html')