# Create your tests here.
import datetime

from django.core.exceptions import ValidationError
from django.http import response
from django.test import TestCase

from .factories import RestaurantFactory, TableFactory, UserFactory
from .forms import BookingForm
from .models import Restaurant


class HomePageTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.restaurant = RestaurantFactory()

    def test_authentication(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_template_rendered(self):
        self.client.force_login(self.user)
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_context_data(self):
        self.client.force_login(self.user)
        response = self.client.get("/")
        context = response.context["restaurants"]

        self.assertEqual(list(context), list(Restaurant.objects.all()))


