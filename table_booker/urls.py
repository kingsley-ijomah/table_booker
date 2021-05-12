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
]
