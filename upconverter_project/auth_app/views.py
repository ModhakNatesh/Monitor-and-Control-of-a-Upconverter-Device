from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            # Create new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')  # Redirect to login after signup

    return render(request, 'auth_app/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('device_status')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'auth_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

