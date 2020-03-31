from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .models import Vehicle, Booking, Schedule, Status, Role
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

BOOKING_STATUS = {
    'BOOKED': 1,
    'DEPARTED': 2,
    'COMPLETED': 4,
    'CANCELLED': 5,
    'ASSIGNED': 6,
}


def index(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.count()
        vehicles = Vehicle.objects.count()
        vendors = 2
        en_route_vehicles = Booking.objects.filter(status_id=BOOKING_STATUS['DEPARTED']).count()
        count = {'bookings': bookings, 'vehicles': vehicles, 'en_route_vehicles': en_route_vehicles, 'vendors': vendors}
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


def new_vehicle_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            make = request.POST['make']
            model = request.POST['model']
            license_plate = request.POST['license_plate']
            role = request.POST['role']

            vehicle = Vehicle.objects.create(make=make, model=model, license_plate=license_plate, role_id=role)
            try:
                vehicle.save()
                return redirect('/vehicles')
            except Exception as e:
                return render(request, 'fms/new-booking.html', {'error_message': e})
        else:
            roles = Role.objects.all()
            return render(request, 'fms/new-vehicle.html', {'roles': roles})
    else:
        return redirect('/login')


def bookings_view(request):
    if request.user.is_authenticated:
        unassigned = Booking.objects.filter(status_id=BOOKING_STATUS['BOOKED']).count()
        completed = Booking.objects.filter(status_id=BOOKING_STATUS['COMPLETED']).count()
        cancelled = Booking.objects.filter(status_id=BOOKING_STATUS['CANCELLED']).count()
        en_route = Booking.objects.filter(status_id=BOOKING_STATUS['DEPARTED']).count()
        count = {'unassigned': unassigned, 'completed': completed,
                 'cancelled': cancelled, 'en_route_vehicles':  en_route}

        bookings = Booking.objects.all()
        return render(request, 'fms/bookings.html', {'bookings': bookings, 'count': count})
    else:
        return redirect('/login')


def new_booking_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            from_location = request.POST['from_location']
            to_location = request.POST['to_location']
            departure_date = request.POST['departure_date']
            purpose = request.POST['purpose']
            description = request.POST['description']
            user_id = request.user.id

            booking = Booking.objects.create(from_location=from_location, to_location=to_location,
                                             description=description, departure_date=departure_date,
                                             purpose_id=purpose, user_id=user_id)
            try:
                booking.save()
                return redirect('/bookings')
            except Exception as e:
                return render(request, 'fms/new-booking.html', {'error_message': e})

        else:
            purposes = Role.objects.all()
            return render(request, 'fms/new-booking.html', {'purposes': purposes})
    else:
        return redirect('/login')


def schedule_view(request):
    if request.user.is_authenticated:
        schedule = Schedule.objects.all()
        return render(request, 'fms/schedule.html', {'schedule': schedule})
    else:
        return redirect('/login')


def new_schedule_view(request):
    if request.user.is_authenticated:
        vehicles = Vehicle.objects.all()
        bookings = Booking.objects.filter(status_id=BOOKING_STATUS['BOOKED']).all()
        if request.method == 'POST':
            departure_arrival_range = request.POST['departure_arrival_range']
            departure_arrival_range = departure_arrival_range.split(" - ")
            departure_date = departure_arrival_range[0]
            arrival_date = departure_arrival_range[1]
            booking_id = request.POST['booking_id']
            vehicle_id = request.POST['vehicle_id']
            existing_vehicle_schedule_count = Schedule.objects.filter(Q(vehicle_id=vehicle_id),
                                                                      Q(departure_date__range=(departure_date,
                                                                                               arrival_date)) |
                                                                      Q(arrival_date__range=(departure_date,
                                                                                             arrival_date))
                                                                      ).count()
            if existing_vehicle_schedule_count > 0:
                return render(request, 'fms/new-schedule.html', {
                    'vehicles': vehicles,
                    'bookings': bookings,
                    'error_message': 'Schedule already exists against given vehicle in the provided time frame. '
                                     'Please adjust your departure and arrival date.'})
            try:
                schedule = Schedule.objects.create(departure_date=departure_date, arrival_date=arrival_date,
                                                   booking_id=booking_id, vehicle_id=vehicle_id)
                schedule.save()
                booking = Booking.objects.get(id=booking_id)
                booking.status_id = BOOKING_STATUS['ASSIGNED']
                booking.save()
                return redirect('/schedule')
            except Exception as e:
                return render(request, 'fms/new-schedule.html', {
                    'vehicles': vehicles,
                    'bookings': bookings,
                    'error_message': 'Unable to create a new schedule. Please try again later.'})

        else:
            return render(request, 'fms/new-schedule.html', {'vehicles': vehicles, 'bookings': bookings})
    else:
        return redirect('/login')


def vendors_view(request):
    if request.user.is_authenticated:
        return render(request, 'fms/vendors.html')
    else:
        return redirect('/login')


def new_vendor_view(request):
    if request.user.is_authenticated:
        return render(request, 'fms/new-vendor.html')
    else:
        return redirect('/login')


@csrf_exempt
def set_booking_status(request):
    try:
        booking = Booking.objects.get(id=int(request.POST['booking_id']))
        booking.status_id = int(request.POST['status_id'])
        booking.save()
        return JsonResponse({'response': 1, 'status': 0})
    except Exception as e:
        return JsonResponse({'response': 1, 'status': -1})



