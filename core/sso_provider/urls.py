from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_captcha/", views.get_captcha, name="get_captcha"),
    path("get_otp/", views.get_otp, name="get_otp"),
    path("get_vid/", views.get_vid, name="get_vid"),
    path("get_data/", views.get_data, name="get_data"),
    path("get_ekyc/", views.get_ekyc, name="get_ekyc"),
    path("vid/", views.vid, name="vid"),
    path("data/", views.data, name="data"),
    path("ekyc/", views.ekyc, name="ekyc"),
]
