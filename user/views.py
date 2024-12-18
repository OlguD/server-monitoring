from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User as AuthUser
from .models import User

# Create your views here.

def login(request):
    if request.method == "POST":
        username: str = request.POST.get('username')
        password: str = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'user/login.html')

    return render(request, 'user/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')

        # Boş alan kontrolü
        if not username or not password or not email or not password1:
            messages.error(request, 'Please fill in all fields')
            return render(request, 'user/register.html')

        # Username kontrolü
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'user/register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'user/register.html')

        if password != password1:
            messages.error(request, 'Passwords do not match')
            return render(request, 'user/register.html')

        try:
            # Önce authentication için User oluştur
            auth_user = AuthUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Sonra sizin User modelinize kaydet
            user = User.objects.create(
                username=username,
                email=email,
                password=password  # Burada hash'lenmiş şifreyi kullanabilirsiniz: auth_user.password
            )
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'An error occurred during registration')
            return render(request, 'user/register.html')

    return render(request, 'user/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')