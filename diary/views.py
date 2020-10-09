from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import requests
import json
from .models import Entry, Game

# Create your views here.

class loginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class registerForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())
    confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput(), label="Confirm Password")

def index(request):
    if not request.user.username:
        print("culo")
        return HttpResponseRedirect(reverse("login"))
    entrylist = Entry.objects.filter(user__username=request.user.username)
    playinglist = Entry.objects.filter(user__username=request.user.username, status="Playing")
    return render(request, "diary/index.html", {
        "entrylist": entrylist,
        "playinglist": playinglist
    })

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

def view(request):
    result= {}
    finishedEntries = Entry.objects.filter(user__username=request.user.username, status="Finished")
    for entry in finishedEntries :
        print(entry.id)
        yearStarted = entry.started.year
        monthStarted = entry.started.month
        yearFinished = entry.finished.year
        monthFinished = entry.finished.month
        if yearFinished not in result:
            result[yearFinished] = {}
            result = sorted(result.items(), reverse= True)
            result = dict(result)
        if monthFinished not in result[yearFinished]:
            result[yearFinished][monthFinished] = {"started": [], "finished": [], "continued": []}
            result[yearFinished] = sorted(result[yearFinished].items(), reverse= True)
            result[yearFinished] = dict(result[yearFinished])
        if yearStarted not in result:
            result[yearStarted] = {}
            result = sorted(result.items(), reverse= True)
            result = dict(result)
        if monthStarted not in result[yearStarted]:
            result[yearStarted][monthStarted] = {"started": [], "finished": [], "continued": []}
            result[yearStarted] = sorted(result[yearStarted].items(), reverse= True)
            result[yearStarted] = dict(result[yearStarted])
        result[yearStarted][monthStarted]["started"].append(entry)
        result[yearFinished][monthFinished]["finished"].append(entry)
    print(result)
    return render(request, "diary/view.html", {
        "gamelist": result,
    })

def entry(request, entryid):
    try:
        entry = Entry.objects.get(id=entryid, user__username=request.user.username)
    except Entry.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "diary/entry.html", {
        "entry": entry
    })