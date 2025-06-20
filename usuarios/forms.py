from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    nome = forms.CharField()
    
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email","nome")


class CustomUserChangeForm(UserChangeForm):
    password = None  

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']