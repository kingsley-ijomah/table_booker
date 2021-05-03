from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    postcode = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


DAYS_OF_WEEK = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
)


class BusinessHour(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Setting(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    advance_booking = models.IntegerField()
    min_guest = models.IntegerField()
    max_guest = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
