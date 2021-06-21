import datetime

import factory
from django.contrib.auth.models import User

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "jacob"
    email = "jacob@email.com"
    password = factory.PostGenerationMethodCall("set_password", "top-secret")


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Restaurant

    name = "Golden Star Restaurant"
    address1 = "20 Temple Road"
    address2 = "London"
    postcode = "E17 8BL"


class TableFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Table

    restaurant = factory.SubFactory(RestaurantFactory)
    name = "Corner Table"
    capacity = 6


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Booking

    user = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    table = factory.SubFactory(TableFactory)
    date = datetime.date.today() + datetime.timedelta(days=1)  # tomorrow
    total_guests = 3


class BusinessHourFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BusinessHour

    restaurant = factory.SubFactory(RestaurantFactory)
    day = 1
    start_time = datetime.time(9, 30, 00)
    finish_time = datetime.time(17, 00, 00)
    closed = False


class SettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Setting

    restaurant = factory.SubFactory(RestaurantFactory)
    min_guest = 2
