from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.

def login(request):
    if request.method == "POST":
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')
        user = User.objects.filter(username=username, password=password)
        if user:
            messages.success(request, 'Login successful')
            return redirect('dashboard')
        else:
            messages.error(request, 'Login failed, check your username and password')

    return render(request, 'user/login.html')

def register(request):
    if request.method == "POST":
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')
        email: str = request.POST.get('email')
        user = User.objects.create(username=username, password=password, email=email)
        return redirect('login')

    return render(request, 'user/register.html')

def logout(request):
    return render(request, 'user/logout.html')