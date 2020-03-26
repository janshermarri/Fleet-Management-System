from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .models import Vehicle, Booking, Schedule, Status, Role


def index(request):
    if request.user.is_authenticated:
        bookings_count = Booking.objects.count()
        vehicles_count = Vehicle.objects.count()
        vendors_count = 2
        count = {'bookings': bookings_count, 'vehicles': vehicles_count, 'vendors': vendors_count}
        return render(request, 'fms/index.html', {'count': count})
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


def vehicles_view(request):
    if request.user.is_authenticated:
        vehicles = Vehicle.objects.all()
        return render(request, 'fms/vehicles.html', {'vehicles': vehicles})
    else:
        return redirect('/login')


def bookings_view(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.all()
        return render(request, 'fms/bookings.html', {'bookings': bookings})
    else:
        return redirect('/login')


def schedule_view(request):
    if request.user.is_authenticated:
        schedule = Schedule.objects.all()
        return render(request, 'fms/schedule.html', {'schedule': schedule})
    else:
        return redirect('/login')


def vendors_view(request):
    if request.user.is_authenticated:
        return render(request, 'fms/vendors.html')
    else:
        return redirect('/login')
