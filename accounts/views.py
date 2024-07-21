from django.shortcuts import render, redirect
from Core.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
import random
import string

# Create your views here.
def randomString(stringlength=6):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringlength))

code = randomString()

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        user = User

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'password': password,
        }

        if password == password2:
            if user.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                if user.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already used')
                    return redirect('register')
                else:
                    if user.objects.filter(phone=phone).exists():
                        messages.error(request, 'Phone number is already used')
                        return redirect('register')
                    else:
                        send_mail(
                            'Account creation confirmed',
                            'Hi '+ first_name + ', Your confirmation code is: '+code,
                            'joyolonga@gmail.com',
                            [email],
                            fail_silently=False
                        )
                        request.method = 'GET'
                        return render(request, 'accounts/confirmregister.html', context)
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def confirmregister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirmcode = request.POST['confirmcode']
        user = User

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'password': password,
        }
        if code == confirmcode:
            user = user.objects.create_user(username=username, password=password, email=email, phone=phone, first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid confirmation code')
            return render(request, 'accounts/confirmregister.html', context)
    else:
        return redirect('register')

def userlogin(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'accounts/login.html')

def userlogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You are now logged out")
        return redirect('index')

