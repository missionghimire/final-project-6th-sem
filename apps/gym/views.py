from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm

from apps.gym.forms import CustomUserForm

def home(request):
    context=dict()
    return render(request,'pages/index.html',context)

def signup(request):
    context=dict()
    if(request.method =='POST'):
        form=CustomUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            # login(request,user)
            return redirect('/')

    else:
        form = CustomUserForm()
        
    
    return render(request,'pages/signup.html',{'form':form}) 

def Logout (request):
    logout(request)
    return redirect('/')

def signin(request):
    if request.method =='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('gym:sigin')
    else:
        form = AuthenticationForm()
        return redirect('gym:signin')
    return render(request,'pages/signin.html',{'form':form})                
