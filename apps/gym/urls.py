from os import abort
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views

from apps.gym.views import Logout, about, approve, becomemember, contact, delete, home, service, signin, signup, trainer, userprofil, update

app_name = 'gym'

urlpatterns = [
    path('', home, name='home'),
    path('signup', signup, name='signup'),
    path('logout/', Logout, name='logout'),
    path('signin', signin, name='signin'),
    path('member', becomemember, name='member'),
    path('memberupdate/<int:pk>', update, name="memberupdate"),
    path('userprofil/<int:pk>', userprofil, name='userprofil'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('approve', approve, name='approve'),
    path('service', service, name='service'),
    path('contact', contact, name='contact'),
    path("about", about, name='about'),
    path('trainer',trainer,name='trainer')
]
