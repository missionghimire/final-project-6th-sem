from django import forms

from django.contrib.auth.forms import UserCreationForm
from apps.gym.models import Contact, CustomUser, Member, Dietmanagement


class CustomUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = (
            'full_name',
            'username',
            'email',
            'number',
            'address',
            'image'
        )
class UserUpdateForm(forms.ModelForm):
     class Meta:
        model = CustomUser
        fields = (
            'full_name',
            'username',
            'number',
            'address',
            'image',
            
        )



class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        exclude = ('is_approved', 'user','status')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'joindate': forms.DateInput(attrs={'type': 'date'}),
            'expiredate': forms.DateInput(attrs={'type': 'date'})
        }


class Formbmi(forms.ModelForm):

    class Meta:
        model = Dietmanagement
        exclude = ('result','user')


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('__all__')
