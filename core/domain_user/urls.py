from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("login/", views.loggin, name="login"),
    path("logout/", LogoutView.as_view(next_page="dashboard"), name="logout"),
    path('add_domain/',views.add_domain,name='add_domain'),
    path("api/check_permission/", views.check_permission, name="check_permission"),
    path("edit_domain/<str:domain_key>/", views.edit_domain, name="edit_domain"),
    path("delete_domain/<str:domain_key>/", views.delete_domain, name="delete_domain"),
]
