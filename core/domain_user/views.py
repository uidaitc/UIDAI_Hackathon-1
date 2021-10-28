from django.db import models
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from domain_user.models import CustomUser
# Create your views here.
def loggin(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect(dashboard)
        else:
            return render(request, 'domain_user/login.html',{'error':'Email or password is incorrect'})
    return render(request, 'domain_user/login.html',{'error':''})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            try:
                user = CustomUser.objects.create_user(email, password)
                user.save()
                return redirect(loggin)
            except:
                return render(request, 'domain_user/register.html',{'error':'Email already exists'})
        else:
            return render(request, 'domain_user/register.html',{'error':'Password and Confirm Password does not match'})
    return render(request, 'domain_user/register.html')

def dashboard(request):
    return render(request, 'domain_user/dashboard.html')
