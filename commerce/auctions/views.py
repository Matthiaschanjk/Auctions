from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    entry = entries.objects.all().order_by('-timestamp')

    return render(request, "auctions/index.html",{
        "entries": entry
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        url = request.POST["url"]
        details = request.POST["details"]
        bid = request.POST["bid"]
        category = request.POST["category"]
        username = request.user.username
        user = User.objects.get(username=username)
        
        listing = entries(user=user, highestbiduser=user,title=title, image=url, detail=details, bid=bid, category=category)
        listing.save()
        
        return render(request, "auctions/index.html", {
            "entries": entries.objects.all()
        })

    else:   
        return render(request, "auctions/create.html")

def list(request, id):
    try:
        entry = entries.objects.get(id=id)
    except:
        return redirect('index')

    oldbid = new_bid.objects.filter(entry_id= id).values_list('bid', flat=True)
    username = request.user

    try:
        userwatchlist = user_watchlist.objects.filter(user=username).get(entry=entry)
    except:
        userwatchlist = 0


    return render(request, "auctions/listing.html", {
        "entry": entry,
        "comment": comments.objects.filter(title=entry),
        "oldbid": oldbid,
        "watchlist": userwatchlist
    })

@login_required(login_url="/login")
def commenting(request, id):
    if request.method == "POST":
        try:
            entry = entries.objects.get(id=id)
        except:
            HttpResponseRedirect(reverse("list"))

        text = request.POST["comment"]
        username = request.user.username
        title = entry

        user_instance = User.objects.get(username=username)
        review = comments(user=user_instance, title=title, comment=text)
        review.save()
        return HttpResponseRedirect(reverse("list", args=[id]))
    
    else:
        return index(request)

@login_required(login_url ="/login")
def newbid(request, id):
    if request.method == "POST":
        try:
            entry = entries.objects.get(id=id)
        except:
            HttpResponseRedirect(reverse("list"))

        newbid = request.POST["newbid"]
        currentbid = entry.bid
        username_name = request.user.username
        username = User.objects.get(username=username_name)
        title = entry
        
        if int(newbid) > int(currentbid):
            lowerbid = new_bid(user=username, entry = title, bid = currentbid)
            lowerbid.save()
            entry.bid = newbid
            entry.save()
            entry.highestbiduser = username_name
            entry.save()
            return HttpResponseRedirect(reverse("list",args=[id]))

        else:
            return HttpResponse("New bid amount must be higher than the current bid")

    else:
        return index(request)

def closed(request):
    return render(request, "auctions/closed.html", {
        "closed": closed_entries.objects.all().order_by('-timestamp')
    })

def closing(request, id):
    if request.method == "POST":
        try:
            entry = entries.objects.get(id=id)
        except:
            HttpResponseRedirect(reverse("list"))
        
        update_entry = closed_entries(user = entry.user, highestbiduser = entry.highestbiduser, title = entry.title, image = entry.image, detail = entry.detail, bid = entry.bid)
        
        try:
            update_entry.save()
        except:
            return HttpResponse("Deal did not close properly")
        
        entry.delete()
        return closed(request)
    
    else:
        return index(request)

def closinglist(request, id):
    try:
        entry = closed_entries.objects.get(id=id)
    except:
        HttpResponseRedirect(reverse("closing"))
    
    return render(request, "auctions/closinglist.html", {
        "entry": entry
    })

@login_required(login_url="/login")
def watchlist(request):
    username = request.user
    entry = user_watchlist.objects.filter(user=username)

    return render(request, "auctions/watchlist.html", {
        "entry": entry
    })

@login_required(login_url="/login")
def watchlist_save(request, id):
    if request.method == "POST":
        try:
            entry = entries.objects.get(id=id)
        except:
            HttpResponseRedirect(reverse("list"))
        
        username = request.user
        userwatchlist = user_watchlist.objects.filter(user=username)

        Addtowatchlist = user_watchlist(user = username, entry = entry)
        Addtowatchlist.save()
        return watchlist(request)
    
    else:
        return index(request)

def watchlist_remove(request, id):
    try:
        entry = entries.objects.get(id=id)
        user = request.user
    except:
        return index

    delete_entry = user_watchlist.objects.filter(user=user).get(entry=entry)
    delete_entry.delete()

    return watchlist(request)

def sort(request, cat):
    try:
        entry = entries.objects.filter(category=cat)
    except:
        return index(request)
    return render(request, "auctions/sort.html", {
        "entries": entry,
        "category": cat
    })



    
        

    