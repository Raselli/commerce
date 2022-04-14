from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "start_bid", "img_url")
            
        widget = {
            "description": forms.Textarea()
        }
        
        labels = {
            "title": "Title of listing item",
            "Description": "Description of listing item",
            "start_bid": "Staring Bid $:",
            "img_url": "Add an URL of your listing:"
        }

def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
              
    # method == GET
    else:
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm()
        })

def listing():
    #TO DO
    pass

def watchlist():
    #TO DO
    pass

def categories():
    #TO DO
    pass

def bidding(request):
    # add lock to prevent bidding collision
    bid = request.Post("bid")
    if Listing.current_bid == Listing.starting_bid:
        if bid < Listing.starting_bid:
            message = "Your bid must be equal to or higher than starting bid."
            return message
        else:
            pass
    elif Listing.current_bid > Listing.starting_bid:
        if Listing.current_bid < bid:
            pass
        else:
           message = "Your bid must be higher than the currently highest bid."
           return message

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
