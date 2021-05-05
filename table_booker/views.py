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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("table_booker:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form},
    )


def signup_page(request):
    return render(request, "signup.html", context={})


def logout_page(request):
    return render(request, "logout.html", context={})
