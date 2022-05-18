from dataclasses import field
from django import forms

from django.contrib.auth.forms import UserCreationForm
from apps.gym.models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('full_name','username','email')