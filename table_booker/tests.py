# Create your tests here.
import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase

from .factories import BookingFactory, RestaurantFactory, TableFactory, UserFactory
from .forms import BookingForm, UserForm
from .models import Restaurant, Table


class HomePageTests(TestCase):
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


class LoginPageTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = "/login"
        self.response = self.client.get(self.url)

    def test_blank_login_page(self):
        context_form = self.response.context["login_form"]

        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(context_form, AuthenticationForm)
        self.assertTemplateUsed(self.response, "login.html")

    def test_successful_login(self):
        data = {
            "username": self.user.username,
            "password": "top-secret",
        }
        response = self.client.post(self.url, data, follow=True)

        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "info")
        self.assertTrue(
            f"You are now logged in as {self.user.username}." in message.message
        )
        self.assertRedirects(response, "/", status_code=302)

    def test_unsuccessful_login(self):
        data = {
            "username": self.user.username,
            "password": "wrong-password",
        }
        response = self.client.post(self.url, data, follow=True)

        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue("Invalid username or password." in message.message)


class SignUpPageTests(TestCase):
    def setUp(self):
        self.url = "/signup"
        self.response = self.client.get(self.url)

    def test_blank_signup_form(self):
        context_form = self.response.context["register_form"]

        self.assertEqual(self.response.status_code, 200)
        self.assertIsInstance(context_form, UserForm)
        self.assertTemplateUsed(self.response, "signup.html")

    def test_successful_signup(self):
        data = {
            "first_name": "Cheikh",
            "last_name": "Anta Diop",
            "username": "cheikh",
            "email": "cheikh@email.com",
            "password1": "top-secret",
            "password2": "top-secret",
        }
        response = self.client.post(self.url, data, follow=True)

        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "success")
        self.assertTrue("Registration successful." in message.message)
        self.assertRedirects(response, "/", status_code=302)

    def test_unsuccessful_signup(self):
        data = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data, follow=True)

        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "error")
        self.assertTrue(
            "Unsuccessful registration. Invalid information." in message.message
        )


class LogoutPageTests(TestCase):
    def setUp(self):
        self.url = "/logout"
        self.response = self.client.get(self.url, follow=True)

    def test_logout(self):
        message = list(self.response.context.get("messages"))[0]

        self.assertEqual(message.tags, "info")
        self.assertEqual(message.message, "You have successfully logged out.")
        self.assertRedirects(self.response, "/login", status_code=302)


class BookingRestaurantTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.restaurant = RestaurantFactory()
        self.table = TableFactory(restaurant=self.restaurant)
        self.url = f"/book-restaurant/{self.restaurant.id}"

    def test_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_invalid_restaurant_id(self):
        self.client.force_login(self.user)
        url = "/book-restaurant/99999"

        response = self.client.get(url, follow=True)
        message = list(response.context.get("messages"))[0]

        self.assertEqual(message.tags, "error")
        self.assertTrue("Invalid restaurant supplied" in message.message)
        self.assertRedirects(response, "/", status_code=302)

    def test_get_blank_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, follow=True)
        context_form = response.context["booking_form"]

        self.assertTemplateUsed(response, "book_restaurant.html")
        self.assertIsInstance(context_form, BookingForm)

    def test_successful_post(self):
        self.client.force_login(self.user)
        data = {
            "user": self.user,
            "restaurant": self.restaurant.id,
            "table": self.restaurant.tables.first().id,
            "date": (datetime.datetime.today() + datetime.timedelta(days=3)).strftime(
                "%Y-%m-%dT%H:%M"
            ),
        }
        response = self.client.post(self.url, data, follow=True)
        message = list(response.context.get("messages"))[0]
        self.assertEqual(message.tags, "info")
        self.assertTrue(f"You successfully booked {self.restaurant}" in message.message)
        self.assertRedirects(response, "/", status_code=302)

    def test_table_queryset(self):
        TableFactory()

        self.client.force_login(self.user)
        response = self.client.get(self.url, follow=True)
        context_form = response.context["booking_form"]

        expected_queryset = context_form.fields["table"].queryset
        queryset = Table.objects.filter(restaurant_id=self.restaurant.id)

        self.assertEqual(list(expected_queryset), list(queryset))


class MyBookingsTests(TestCase):
    def setUp(self):
        self.user1 = UserFactory(username="Jane")
        self.user2 = UserFactory(username="Bayo")
        self.booking1 = BookingFactory(user=self.user1)
        self.booking2 = BookingFactory(user=self.user2)
        self.url = "/my-bookings"

    def test_authentication(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, "/login", status_code=302)

    def test_template_rendered(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "my_bookings.html")

    def test_user1_context_data(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        context = response.context["bookings"]
        self.assertEqual(list(context), [self.booking1])

    def test_user2_context_data(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        context = response.context["bookings"]
        self.assertEqual(list(context), [self.booking2])

