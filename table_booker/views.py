# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .models import Restaurant


def home_page(request):
    if not request.user.is_authenticated:
        return redirect("table_booker:login")

    context = {"restaurants": Restaurant.objects.all()}
    return render(request, "home.html", context=context)


def login_page(request):
    return render(request, "login.html", context={})


def signup_page(request):
    return render(request, "signup.html", context={})


def logout_page(request):
    return render(request, "logout.html", context={})
