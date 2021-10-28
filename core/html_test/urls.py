from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("captcha/", views.get_captcha),
    path("otp/", views.get_otp),
    
]
