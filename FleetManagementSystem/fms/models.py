from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=30)
    remarks = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.make, self.model)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purpose = models.ForeignKey(Role, on_delete=models.CASCADE)
    items = models.CharField(max_length=50)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    description = models.TextField(null=True, default=None)
    departure_date = models.DateTimeField()
    from_location = models.TextField(max_length=255)
    to_location = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_created=True)
    date_updated = models.DateTimeField(auto_now=True)


class Schedule(models.Model):
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
