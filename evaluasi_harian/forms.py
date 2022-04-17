from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class LoginForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'password']
    widgets = {
      'username': forms.TextInput(attrs={'class': 'input'}),
      'password': forms.PasswordInput(attrs={'class': 'input'}),
    }