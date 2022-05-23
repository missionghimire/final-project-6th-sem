from dataclasses import field
from django import forms

from django.contrib.auth.forms import UserCreationForm
from apps.gym.models import CustomUser,Member,Dietmanagement, Passwordreset


class CustomUserForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('full_name','username','email',)


class MemberForm(forms.ModelForm):
    class Meta:
        model=Member
        exclude=('is_approved','user')
        widgets = {
            'date_of_birth':forms.DateInput(attrs={'type':'date'}),
            'joindate':forms.DateInput(attrs={'type':'date'}),
            'expiredate':forms.DateInput(attrs={'type':'date'})
        }

class Formbmi(forms.ModelForm):
    class Meta:
        model=Dietmanagement
        fields=('__all__')

class Password_reset(forms.ModelForm):
    class Meta:
        model=Passwordreset
        fields=('__all__')
        
