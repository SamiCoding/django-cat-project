from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='사용자 이름')
    class Meta(UserCreationForm.Meta):
        model = User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='사용자 이름')