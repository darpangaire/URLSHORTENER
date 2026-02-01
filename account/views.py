from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# verified email :

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password1']
      phone_number = form.cleaned_data['phone_number']
      username = email.split('@')[0] # Extract username from email
      
      user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
      user.phone_number = phone_number
      user.is_active = True  # Set user as active upon registration
      user.save()
      messages.success(request,'Registration Successful.')
      return redirect('login')
    
    else:
      messages.error(request,'Invalid Information')
      
  else:
    form = RegistrationForm()
  return render(request,'account/register.html',{'form':form})
    
      
def Login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(request,email=email,password=password)
    
    if user is not None:
      login(request,user)
      messages.success(request,'Login Successful.')
      return redirect('home')
    else:
      messages.error(request,'Invalid login credentials')
      return redirect('login')
    
  return render(request,'account/login.html')

