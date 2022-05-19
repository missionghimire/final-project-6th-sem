from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.gym.forms import CustomUserForm, MemberForm

def home(request):
    context=dict()
    return render(request,'pages/index.html',context)

def signup(request):
    context=dict()
    if(request.method =='POST'):
        form=CustomUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request,'Login Success')
            
            return redirect('gym:signin')

    else:
        form = CustomUserForm()
        
    
    return render(request,'pages/signup.html',{'form':form}) 

def Logout (request):
    logout(request)
    messages.success(request,'Logout Success')
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
                return redirect('/')
    else:
        form = AuthenticationForm()
        
       
    return render(request,'pages/signin.html',{'form':form}) 
    
     
@login_required(login_url='gym:signin')
def becomemember(request):
    context=dict()
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if(form.is_valid):
            data=form.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Member Added')
            return redirect('/')
    else:
        form=MemberForm()

    context['form']=form            
    
    return render(request,'pages/becomemember.html',context)
