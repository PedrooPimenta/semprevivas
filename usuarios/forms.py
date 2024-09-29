from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    nome = forms.CharField()
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email","nome")

