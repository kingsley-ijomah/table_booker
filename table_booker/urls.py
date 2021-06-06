from django.urls import path

from . import views

app_name = "table_booker"

urlpatterns = [
    path("", views.home_page, name="home"),
    path("login", views.login_page, name="login"),
    path("logout", views.logout_page, name="logout"),
    path("signup", views.signup_page, name="signup"),
    path(
        "book-restaurant/<int:restaurant_id>",
        views.book_restaurant,
        name="book-restaurant",
    ),
    path("my-bookings", views.my_bookings, name="my-bookings"),
    path(
        "delete-booking/<int:booking_id>", views.delete_booking, name="delete-booking"
    ),
    path(
        "update-booking/<int:booking_id>", views.update_booking, name="update-booking"
    ),
]
