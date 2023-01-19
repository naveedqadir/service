from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from .forms import ContactForm,NewsLetterForm
from django.contrib.auth.decorators import login_required
from urllib.request import urlopen
import json


# Create your views here.
def home(request):
    form = NewsLetterForm()
    return render(request,'tcsion/index.html',{'form':form})

def contact(request):
    form=ContactForm()
    # print(form)
    if(request.method=='POST'):
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()        
            #return redirect('home')
            return render (request,'tcsion/contact.html',{'message':'Message Sent Successfully'})
    return render(request,'tcsion/contact.html', {'form':form})

@login_required
def services(request):
    url = "https://api.quotable.io/random"
    response = urlopen(url)
    data_json = json.loads(response.read())
    mydata=data_json['content']
    return render(request,'tcsion/services.html',{'message':mydata})

def about(request):
    return render(request,'tcsion/about.html')

def newsletter(request):
    if request.method=='POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return render (request,'tcsion/index.html',{'message':'Sucessfully Subscribed to Newsletter'})
        else:
            return render (request,'tcsion/index.html',{'message':'Email already exists'})

def account(request):
    return render(request,'tcsion/account.html')
    
def loginuser(request):
    if request.method == 'GET':
        return render(request,'tcsion/loginuser.html',{'form':AuthenticationForm()})
    else:
        uname= request.POST['username']
        upswd= request.POST['password']
        user=authenticate(request, username=uname, password=upswd)
        if user is not None:
            login(request,user)
            return redirect('account')
        else:
            return render(request,'tcsion/loginuser.html',{'form':AuthenticationForm(),'message':'User not found,Try again'})

def logoutuser(request):
    logout(request)   
    return redirect('home') 

def signupuser(request):   
    if request.method == 'GET':
        return render(request,'tcsion/signupuser.html',{'form':UserCreationForm()})
    else:
        uname = request.POST['username']
        upswd1 = request.POST['password1']
        upswd2 = request.POST['password2']
        if upswd1==upswd2:
            try:
                user = User.objects.create_user(username=uname,password=upswd1)
                user.save()
                login(request,user)
            except IntegrityError:
                return render(request,'tcsion/signupuser.html',{'form':UserCreationForm(),'message':'Username already Exist'})
            else:
                return redirect('account')
        else:
             return render(request,'tcsion/signupuser.html',{'form':UserCreationForm(),'message':'Password Mismatch'})

