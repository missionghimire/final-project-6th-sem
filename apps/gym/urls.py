from django.urls import path

from apps.gym.views import home

app_name='gym'


 
urlpatterns = [
    path('',home,name='home')
] 