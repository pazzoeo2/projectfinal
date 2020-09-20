from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse

# Create your views here.

class loginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class registerForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="Confirm Password")

def index(request):
    return render(request, "diary/index.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "diary/login.html", {
                "message": "Invalid username and/or password.",
                "form": loginForm()
            })
    else:
        return render(request, "diary/login.html", {
            "form": loginForm()
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "diary/register.html", {
                "message": "Passwords must match.",
                "form": registerForm()
            })

        try:
            user = User.objects.create_user(username, password)
            user.save()
        except IntegrityError:
            return render(request, "diary/register.html", {
                "message": "Username already taken.",
                "form": registerForm()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "diary/register.html", {
            "form": registerForm()
        })