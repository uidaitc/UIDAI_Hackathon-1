from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from domain_user.models import CustomUser, Domain
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth.decorators import login_required

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
    data = {}
    if request.user.is_authenticated:
        data["domains"] = Domain.objects.filter(user=request.user)
    return render(request, "domain_user/dashboard.html", data)


@csrf_exempt
@api_view(["POST"])
def check_permission(request):
    try:
        domain = Domain.objects.filter(
            domain=request.data["origin"], domain_key=request.data["apikey"]
        )
        if domain:
            permissions = set(domain[0].permission.split(",")).intersection(
                set(json.loads(request.data["permissions"]))
            )
            print(permissions)
            return Response(
                data={"result": True, "permissions": permissions},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"result": False, "permissions": {}}, status=status.HTTP_200_OK
            )
    except:
        return Response(data={}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def add_domain(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized")
    else:
        if request.method == "GET":
            return render(request, "domain_user/domain_add.html")
        elif request.method == "POST":
            temp = []
            for i in range(1, 6):
                try:
                    temp.append(request.POST[f"perm{i}"])
                except:
                    pass
            perm = ",".join(temp)
            Domain.objects.create(
                domain=request.POST["domain"],
                ekycxml_endpoint=request.POST["ekycxml_endpoint"],
                permission=perm,
                user=request.user,
            )
            return redirect(dashboard)


@login_required
def edit_domain(request, domain_key):
    if request.method == "GET":
        domain = Domain.objects.filter(domain_key=domain_key, user=request.user)
        if domain:
            domain = domain[0]
            temp = {}
            temp["domain"] = domain.domain
            temp["ekycxml_endpoint"] = domain.ekycxml_endpoint
            temp["permission"] = []
            perm = domain.permission.split(",")
            print(perm)
            for i in range(1, 6):
                if f"p{i}" in perm:
                    temp["permission"].append("checked")
                else:
                    temp["permission"].append("")
            print(temp)
            return render(
                request, "domain_user/domain_edit.html", {"domain": temp}
            )
        else:
            return HttpResponse("Domain not found")
    if request.method == "POST":
        temp = []
        for i in range(1, 6):
            try:
                temp.append(request.POST[f"perm{i}"])
            except:
                pass
        perm = ",".join(temp)
        domain = Domain.objects.get(
            domain_key=domain_key
        )
        domain.domain = request.POST["domain"]
        domain.ekycxml_endpoint = request.POST["ekycxml_endpoint"]
        domain.permission = perm
        domain.save()
        return redirect(dashboard)


@login_required
def delete_domain(request, domain_key):
    domain = Domain.objects.filter(domain_key=domain_key, user=request.user)
    if domain:
        domain = domain[0]
        domain.delete()
        return redirect(dashboard)
    else:
        return HttpResponse("Domain not found")
