from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from datetime import date
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
    if not request.user.username:
        return HttpResponseRedirect(reverse("login"))
    # This code makes sure every entry is handed off to the HTML template in correct cronological order by storing them in dictionaries for
    # months and years, creating them if they're not present and sorting them every time one is created
    result= {}
    finishedEntries = Entry.objects.filter(user__username=request.user.username)
    for entry in finishedEntries :
        yearStarted = entry.started.year
        monthStarted = entry.started.month
        if entry.status == "Finished":
            # This adds games to the "Finished" column
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
            result[yearFinished][monthFinished]["finished"].append(entry)
        # This adds games to the "Started" column
        if yearStarted not in result:
            result[yearStarted] = {}
            result = sorted(result.items(), reverse= True)
            result = dict(result)
        if monthStarted not in result[yearStarted]:
            result[yearStarted][monthStarted] = {"started": [], "finished": [], "continued": []}
            result[yearStarted] = sorted(result[yearStarted].items(), reverse= True)
            result[yearStarted] = dict(result[yearStarted])
        result[yearStarted][monthStarted]["started"].append(entry)
        # This codes populates the "Playing" column by going through every month from the "started" date, to the "finished" date, or the current date if the
        # game is being currently played. In a future version, this will be calculated by checking if the game has been played for any amount of hours
        # during that month
        stop = False
        while stop == False:
            if entry.status == "Finished":
                if monthStarted > monthFinished and yearStarted >= yearFinished:
                    stop = True
                    continue  
            else:
                if monthStarted > date.today().month and yearStarted >= date.today().year:
                    stop = True
                    continue
            if yearStarted not in result:
                result[yearStarted] = {}
                result = sorted(result.items(), reverse= True)
                result = dict(result)
            if monthStarted not in result[yearStarted]:
                result[yearStarted][monthStarted] = {"started": [], "finished": [], "continued": []}
                result[yearStarted] = sorted(result[yearStarted].items(), reverse= True)
                result[yearStarted] = dict(result[yearStarted])
            result[yearStarted][monthStarted]["continued"].append(entry)
            monthStarted += 1
            if monthStarted == 13:
                yearStarted += 1
                monthStarted = 1
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

def add(request):
    if not request.user.username:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "diary/add.html")

def searchquery(request):
    if request.method=="POST":
        data = json.loads(request.body)
        # I'm pretty sure this isn't the best way to store API Keys...
        headers = {
            'Accept': 'application/json',
            'Client-ID': "69tlfuffu7yciq0gwu37rhy0qjtmh0",
            'Authorization': 'Bearer 9mw1ns7alo0eq4un0inl2bsaz1r5ag'
        }
        r = requests.post("https://api.igdb.com/v4/games", headers=headers, data=f'search "{data["searchterm"]}"; fields name, cover.image_id; limit 30;')
        return HttpResponse(r.content)

def addgame(request):
    if request.method=="POST":
        data = json.loads(request.body)
        print(data)
        # This caches the needed game data in the database so that I don't have to make API requests constantly
        if not Game.objects.filter(id=data["gameid"]).exists():
            # Haha API keys again
            headers = {
                'Accept': 'application/json',
                'Client-ID': "69tlfuffu7yciq0gwu37rhy0qjtmh0",
                'Authorization': 'Bearer 9mw1ns7alo0eq4un0inl2bsaz1r5ag'
            }
            r = requests.post("https://api.igdb.com/v4/games", headers=headers, data=f'fields name, cover.image_id; where id = {data["gameid"]};')
            result = json.loads(r.content)
            print(result)
            try:
                g = Game(id=result[0]["id"], name=result[0]["name"], cover=f'https://images.igdb.com/igdb/image/upload/t_cover_big/{result[0]["cover"]["image_id"]}.jpg')
            except:
                return HttpResponse(json.dumps({"success": False, "error": "An error occurred while adding the game to the database."}))
            g.save()
            print("Game Saved")
        game = Game.objects.get(id=data["gameid"])
        if data["finished"] == '':
            finished = None
        else:
            finished = data["finished"]
        if data["completed"] == '':
            completed = None
        else:
            completed = data["completed"]
        if data["timeplayed"] == '':
            timeplayed = 0
        else: 
            timeplayed = int(data["timeplayed"])
        try:
            entr = Entry(user=request.user, game=game, started=data["started"], finished=finished, completed=completed, timeplayed=timeplayed, status=data["status"], review=data["review"])
        except:
            return HttpResponse(json.dumps({"success": False, "error": "An error occurred while creating your diary entry."}))
        entr.save()
        print("Entry Saved")
        lastsaved = Entry.objects.get(user=request.user, game=game, started=data["started"], finished=finished, timeplayed=timeplayed, status=data["status"], review=data["review"])
        return HttpResponse(json.dumps({"success": True, "entryid": lastsaved.id}))

def delete(request):
    if request.method=="POST":
        data = json.loads(request.body)
        try:
            Entry.objects.get(id=data["entry"]).delete()
        except:
            response = json.dumps({"success": False})
            return HttpResponse(response)
        response = json.dumps({"success": True})
        return HttpResponse(response)

def editentry(request):
    if request.method=="POST":
        data = json.loads(request.body)
        entry = Entry.objects.get(id=data["entryid"])
        if data["started"]:
            entry.started = data["started"]
        if data["finished"]:
            entry.finished = data["finished"]
        if data["completed"]:
            entry.completed = data["completed"]
        if data["timeplayed"]:
            entry.timeplayed = data["timeplayed"]
        if data["status"] and data["status"] != "-No change-":
            entry.status = data["status"]
        if data["review"]:
            entry.review = data["review"]
        try:
            entry.save()
        except:
            return HttpResponse(json.dumps({"success": False, "error": "An error occurred while editing the entry."}))
        return HttpResponse(json.dumps({"success": True, "entryid": entry.id}))

def addhours(request):
    if request.method=="POST":
        data = json.loads(request.body)
        entry = Entry.objects.get(id=data["id"])
        if data["hours"] == '':
            return HttpResponse(json.dumps({"success": False}))
        if entry.timeplayed:
            entry.timeplayed += int(data["hours"])
        else:
            entry.timeplayed = int(data["hours"])
        try:
            entry.save()
        except:
            return HttpResponse(json.dumps({"success": False}))
        return HttpResponse(json.dumps({"success": True}))