from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from domain_user.models import CustomUser, Domain
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def loggin(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect(dashboard)
        else:
            return render(
                request,
                "domain_user/login.html",
                {"error": "Email or password is incorrect"},
            )
    return render(request, "domain_user/login.html", {"error": ""})


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password == confirm_password:
            try:
                user = CustomUser.objects.create_user(email, password)
                user.save()
                return redirect(loggin)
            except:
                return render(
                    request,
                    "domain_user/register.html",
                    {"error": "Email already exists"},
                )
        else:
            return render(
                request,
                "domain_user/register.html",
                {"error": "Password and Confirm Password does not match"},
            )
    return render(request, "domain_user/register.html")


def dashboard(request):
    return render(request, "domain_user/dashboard.html")

@csrf_exempt
@api_view(["POST"])
def check_permission(request):
    domain = Domain.objects.filter(
        domain=request.data["origin"], domain_key=request.data["apikey"]
    )
    if domain:
        permissions = set(domain[0].permission.split(",")).intersection(
            set(request.data["permissions"])
        )
        return Response(
            data={"result": True, "permissions": permissions}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            data={"result": False, "permissions": {}}, status=status.HTTP_200_OK
        )
