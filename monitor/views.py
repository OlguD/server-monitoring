from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required(login_url='/user/login')
def dashboard(request):
    return render(request, 'monitor/dashboard.html')

@login_required
def server_list(request):
    return render(request, 'monitor/server_list.html')

@login_required
def monitoring(request):
    return render(request, 'monitor/monitoring.html')

@login_required
def settings(request):
    return render(request, 'monitor/settings.html')