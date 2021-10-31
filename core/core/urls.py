"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import include,url
from . import views
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin


admin.site.site_header = "Aadhaar SSO"
admin.site.site_title = "Aadhaar SSO - Admin Portal"
admin.site.index_title = "Welcome to Aadhaar SSO"
# admin.site.login_template = "domain_user/login.html"
# auth_views.PasswordResetView.template_name = 'password_reset_form.html'
# auth_views.PasswordResetView.email_template_name = 'password_reset_email.html'
# auth_views.PasswordResetDoneView.template_name = 'password_reset_done.html'
# auth_views.PasswordResetConfirmView.template_name = 'password_reset_confirm.html'
# auth_views.PasswordResetCompleteView.template_name = 'password_reset_complete.html'
# auth_views.PasswordChangeView.template_name = 'password_change_form.html'
# auth_views.PasswordChangeDoneView.template_name = 'password_change_done.html'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('html_test/', include('html_test.urls')),
    path('sso/', include('sso_provider.urls')),
    path('user/', include('domain_user.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
]
