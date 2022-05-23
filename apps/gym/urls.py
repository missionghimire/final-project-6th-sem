
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views


from apps.gym.views import Logout, approve, becomemember, delete, home, service, signin, signup, userprofil

app_name='gym'


 
urlpatterns = [
    path('',home,name='home'),
    path('signup',signup,name='signup'),
    path('logout/',Logout,name='logout'),
    path('signin',signin,name='signin'),
    path('member',becomemember,name='member'),
    path('userprofil',userprofil,name='userprofil'),
    path('delete/<int:pk>/',delete,name='delete'),
    
    path('approve',approve,name='approve'),
    path('service',service,name='service'),

    # password reset
  
    # path('reset_password/',
    #  auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
    #  name="reset_password"),

    # path('reset_password_sent/', 
    #     auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
    #     name="password_reset_done"),

    # path('password/reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name='password_reset_confirm'),

    # path('reset_password_complete/', 
    #     auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
    #     name="password_reset_complete"),

    


    
] 