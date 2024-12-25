from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import UserModel

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'user/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')

        # Field validation
        if not username or not password or not email or not password1:
            messages.error(request, 'Please fill in all fields')
            return render(request, 'user/register.html')

        # Username check
        if UserModel.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'user/register.html')
            
        if UserModel.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'user/register.html')

        if password != password1:
            messages.error(request, 'Passwords do not match')  
            return render(request, 'user/register.html')

        try:
            # Create user with UserManager
            user = UserModel.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'An error occurred during registration')
            return render(request, 'user/register.html')

    return render(request, 'user/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')