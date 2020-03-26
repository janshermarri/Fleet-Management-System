from django.contrib import admin

# Register your models here.
from fms.models import Booking, Vehicle, Schedule, Status, Role
admin.site.register(Booking)
admin.site.register(Status)
admin.site.register(Role)
admin.site.register(Vehicle)
admin.site.register(Schedule)