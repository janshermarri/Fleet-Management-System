from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('vehicles/', views.vehicles_view, name='vehicles'),
    path('bookings/', views.bookings_view, name='bookings'),
    path('vendors/', views.vendors_view, name='vendors'),
    path('schedule/', views.schedule_view, name='schedule')
]