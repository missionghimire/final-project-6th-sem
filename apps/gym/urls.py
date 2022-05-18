from unicodedata import name
from django.urls import path

from apps.gym.views import Logout, home, signin, signup

app_name='gym'


 
urlpatterns = [
    path('',home,name='home'),
    path('signup',signup,name='signup'),
    path('logout',Logout,name='logout'),
    path('signin',signin,name='signin'),
] 