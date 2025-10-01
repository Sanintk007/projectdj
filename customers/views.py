from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Customer


def sign_out(request):
    logout(request)
    return redirect('home')
# Create your views here.    
def show_account(request):
    context={}
    # Handle Registration
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            # Create user account (use create_user so password is hashed)
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # Create customer account
            Customer.objects.create(
                name=username,
                user=user,
                phone=phone,
                address=address
            )

            messages.success(request, "User registered successfully!")

        except Exception as e:
            messages.error(request, "Duplicate username or invalid inputs")

    # Handle Login
    if request.POST and 'login' in request.POST:
        context['register']=False
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)

        if user:
            login(request, user)
            return redirect('home')   # Make sure you have a 'home' url
        else:
            messages.error(request, "Invalid user credentials")

    return render(request, 'account.html',context)
