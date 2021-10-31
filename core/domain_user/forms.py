from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser,Domain


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class DomainForm(forms.ModelForm):
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # create meta class
    class Meta:
        # specify model to be used
        model = Domain
        # specify fields to be used
        fields = ['domain','permission','domain_key','ekycxml_endpoint']
