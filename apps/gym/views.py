from multiprocessing import context
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.gym.forms import ContactForm, CustomUserForm, Formbmi, MemberForm, UserUpdateForm
from apps.gym.models import Carausel, CustomUser, Dietmanagement, Enquery, Equipment, Member, Plan, Trainer
from django.core.mail import send_mail
from config import settings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def home(request):
    context = dict()
    
    enquiry = Enquery.objects.all()
    plan = Plan.objects.all()
    equipment = Equipment.objects.all()
    member = Member.objects.all()
    e1 = 0
    p1 = 0
    eq1 = 0
    m1 = 0
    for menquiry in enquiry:
        e1 += 1
    for mplan in plan:
        p1 += 1
    for mequipment in equipment:
        eq1 += 1
    for mmember in member:
        m1 += 1
    context = {'e1': e1, 'p1': p1, 'eq1': eq1, 'm1': m1}
    context['trainers']=Trainer.objects.all()
    context['car']=Carausel.objects.all()
    return render(request, 'pages/index.html', context)

def trainerdetails(request,pk):
    context=dict()
    context['trainerdetails']=Trainer.objects.filter(id=pk)
    return render(request,'pages/trainerdetail.html',context)


def signup(request):

    if (request.method == 'POST'):
        form = CustomUserForm(request.POST, request.FILES)
        if (form.is_valid()):
            form.save()
            messages.success(request, 'Login Success')
            return redirect('gym:signin')
    else:
        form = CustomUserForm()

    return render(request, 'pages/signup.html', {'form': form})


def Logout(request):
    logout(request)
    messages.success(request, 'Logout Success')
    return redirect('/')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/signin.html', {'form': form})


@login_required(login_url='gym:signin')
def becomemember(request):
    context = dict()
    if request.method == 'POST':
        form = MemberForm(request.POST)
        
        if (form.is_valid):
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request, 'Member Added')
            return redirect('gym:approve')
    else:
        form = MemberForm()
    context['form'] = form
    return render(request, 'pages/becomemember.html', context)


@login_required(login_url='gym:signin')
def userprofil(request, pk):

    if request.method == "POST":
        custom = CustomUser.objects.get(id=pk)
        form = UserUpdateForm(request.POST, request.FILES, instance=custom)
        if form.is_valid():
            form.save()
            messages.success(request, "Update Success ")
            return redirect("gym:userprofil", pk)
    else:
        custom = CustomUser.objects.get(id=pk)
        form = UserUpdateForm(instance=custom)

    context = {
        'form': form,
    }
    return render(request, 'pages/userprofil.html', context)


@login_required(login_url='gym:signin')
def delete(request, pk):
    try:
        member = Member.objects.get(id=pk)
        member.delete()
        messages.success(request, 'Membership Deleted')
        return redirect('gym:member')
    except Member.DoesNotExist:
        messages.error(request, 'Membership cant delete')
        return redirect('gym:member')


@login_required(login_url='gym:signin')
def approve(request):
    if (request.user.is_authenticated):
        try:

            info = Member.objects.get(user__id=request.user.id)
            if (info.is_approved):
                user_plan = info.plan
                plan = Plan.objects.get(id=user_plan.id)
                amount_paid = float(info.initialamount)
                if (amount_paid < float(plan.amount)):
                    due_amount = float(plan.amount) - amount_paid
                else:
                    due_amount = 0.0
                context = {
                    'plan': plan,
                    'due_amount': due_amount,
                    'is_approved': True,
                    'info': info
                }
            else:
                context = {'is_approved': False, 'info': info}
        except:
            messages.error(request, 'Add membership first')
            return redirect('gym:member')

    return render(request, 'pages/approved.html', context)


# def service(request):


#     if request.user.is_authenticated:
#         if (request.method == "POST"):
#             context = {}

#             form = Formbmi(request.POST)
#             data = request.POST
#             print(data)
#             height = float(data['height']) / 0.0328084
#             weight = float(data['weight'])
#             print(height, weight)
#             bmi = weight / (height / 100)**2
#             print(bmi, '-------------')
#             if (bmi < 18.5):
#                 context['status'] = "You are underweight"
#             elif (bmi >= 18.5 and bmi < 24.9):
#                 context['status'] = "You are healthy."
#             elif (bmi >= 24.9 and bmi < 29.9):
#                 context['status'] = "You are over weight."
#             elif (bmi <= 34.9):
#                 context['status'] = "You are severely over weight"

#             elif (bmi <= 39.9):
#                 context['status'] = "You are obese"
#             else:
#                 context['status'] = "You are severely obese"

#             return render(request, 'pages/services.html', context)
#         else:
#             form = Formbmi()

#         try:

#             info = Member.objects.get(user__id=request.user.id)
#             if (not info.is_approved):
#                 messages.success(request, 'Admin Approved first')
#                 return redirect('gym:approve')

#         except:
#             messages.error(request, 'Membership first')
#             return redirect('gym:member')
#     else:
#         messages.success(request, 'login first')
        
#         return redirect('gym:signin')

#     return render(request, 'pages/services.html', {'form': form})

# 


@login_required(login_url='gym:signin')
def update(request, pk):
    if request.method == "POST":
        member = Member.objects.get(id=pk)
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Update Success ")
            return redirect("gym:approve")
    else:
        member = Member.objects.get(id=pk)
        form = MemberForm(instance=member)

    context = {
        'form': form,
    }
    return render(request, 'pages/update_member.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            send_mail(str(name) + ' || ' + str(email),
                      message,
                      settings.EMAIL_HOST_USER,
                      settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            messages.success(request, 'Email Send')
            return redirect('gym:contact')

    return render(request, 'pages/contact-us.html', {'form': form})


def about(request):
    context=dict()
    context['plans']=Plan.objects.all()
    return render(request, 'pages/about.html',context)

@login_required(login_url='gym:signin')
def trainer(request):
    context = dict()
    if request.user.is_authenticated:
        trainer = Trainer.objects.get(user__id=request.user.id)
    context['infos'] = Member.objects.filter(trainer__id=trainer.id)
    return render(request, 'pages/trainer.html', context)


def service(request):
   
    return render(request, "pages/services.html")

def predict(request):
    context =dict()
    return render(request,"pages/predict.html", context)

def result(request):
    data = pd.read_csv('bmi.csv')
    data = pd.get_dummies(data)
    data.drop('Gender_Male',axis=1, inplace=True)
    X =data.drop('Index',axis=1)
    y = data['Index']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = LogisticRegression()
    model.fit(X_train,y_train)


    val1 = float(request.GET['Gender'])
    val3 = float(request.GET['Height'])  #/ 0.0328084
    val4 = float(request.GET['Weight'])
    pred = model.predict([[val1,val3,val4]])

    result1 = ""
    
    
    if pred  == [0]:
        result1 = " Weak"
    elif  pred  == [1]:
        result1 = "Extrmly Weak."
    elif   pred  == [2]:
        result1 = "Normal"
    elif  pred == [3]:
        result1 = "You are over weight."
    elif  pred  == [4]:
        result1 = " Obesity"
    elif  pred  == [5]:
        result1 = "Extreme Obesity"
    else:
        result1 = "other"
  
    return render(request, "pages/predict.html",{'result2':result1})
