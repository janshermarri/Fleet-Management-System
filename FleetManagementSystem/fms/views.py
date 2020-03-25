from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return render(request, 'fms/index.html')
    else:
        return redirect('/login')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'fms/login.html', {'error_message': 'Invalid username or password. Try again.'})

    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'fms/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = authenticate(username=username, password=password)

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password)
        try:
            user.save()
            return render(request, 'fms/login.html', {'success_message': 'User account created successfully.'})
        except Exception as e:
            return render(request, 'fms/register.html', {'error_message': e})

    else:
        return render(request, 'fms/register.html')


def logout_user(request):
    logout(request)
    return redirect('/login/')

