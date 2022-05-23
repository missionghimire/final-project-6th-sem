from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.gym.forms import CustomUserForm, Formbmi, MemberForm, Password_reset
from apps.gym.models import Member, Plan


def home(request):
    context = dict()
    # if request.user.is_authenticated:
    #     u = request.user
    #     try:
    #         member = Member.objects.get(user__id=u.id)
    #     except Member.DoesNotExist:
    #         member = None
    #     if member is not None:
    #         return redirect('gym:approve')
            
    #     else:
    #         messages.error(request,'already exits')
    #         return redirect('gym:member')
    return render(request, 'pages/index.html', context)


def signup(request):
    context = dict()
    if (request.method == 'POST'):
        form = CustomUserForm(request.POST)
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
    context=dict()
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if(form.is_valid):
            data=form.save(commit=False)
            data.user=request.user
            data.save()
            messages.success(request,'Member Added')
            return redirect('gym:approve')
    else:
        form=MemberForm()
       

    context['form']=form            
    
    return render(request,'pages/becomemember.html',context)


def userprofil(request):
    return render(request, 'pages/userprofil.html')


def delete(request, pk):
    try:
        member = Member.objects.get(id=pk)
        member.delete()
        messages.success(request, 'Membership Deleted')
        return redirect('gym:member')
    except Member.DoesNotExist:
        messages.error(request, 'Membership cant delete')
        return redirect('gym:member')

def approve(request):
    if(request.user.is_authenticated):
        try:

        
            info  = Member.objects.get(user__id=request.user.id)
            if(info.is_approved):
                user_plan = info.plan
                plan = Plan.objects.get(id=user_plan.id)
                amount_paid = float(info.initialamount)
                if(amount_paid < float(plan.amount)):
                    due_amount = float(plan.amount) - amount_paid
                else:
                    due_amount = 0.0
                context = {
                'plan':plan,
                'due_amount':due_amount,
                'is_approved':True,
                'info':info
                        }
            else:
                context = {'is_approved':False,'info':info}
        except:
            messages.error(request,'Add membership first')
            return redirect('gym:member')        

    return render(request,'pages/approved.html',context)    


def service(request):
    
    if request.user.is_authenticated:
        if(request.method=="POST"):
            context = {}
        
            form = Formbmi(request.POST)
            data  = request.POST 
            print(data)
            height= float(data['height'])/0.0328084
            weight = float(data['weight'])
            print(height,weight)
            bmi = weight / (height/100)**2
            print(bmi,'-------------')
            if(bmi<18.5):
                context['status'] = "You are underweight"
            elif(bmi>=18.5 and bmi <24.9):
                context['status'] = "You are healthy."
            elif(bmi >=24.9 and bmi <29.9):
                context['status'] = "You are over weight."
            elif(bmi <=34.9):
                context['status'] = "You are severely over weight"    
                
            elif(bmi <=39.9):
                context['status'] = "You are obese"
            else:
                context['status'] = "You are severely obese"
                    
            return render(request,'pages/services.html',context)  
        else:
            form = Formbmi()

            

        try:

            info  = Member.objects.get(user__id=request.user.id)
            if( not info.is_approved):
                messages.success(request,'Admin Approved first')
                return redirect('gym:approve')
               
        except:
            messages.error(request,'Membership first')
            return redirect('gym:member')
    else:
        messages.success(request,'login first')     
        return redirect('/')  
            
    return render(request,'pages/services.html',{'form':form})        

# def passwordreset(request):
#     form=Password_reset
#     return render(request,'pages/passwordreset.html',{'form':form})