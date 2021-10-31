from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.loggin, name="login"),
    path("logout/", LogoutView.as_view(next_page="dashboard"), name="logout"),
    path('adddomain/',views.add_domain,name='adddomain'),
    path("api/check_permission/", views.check_permission, name="check_permission"),
]
