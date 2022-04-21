from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment

# Home
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

# Form: new listing
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
        
        
#  create new listing
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        # post form and get foreign key
        form = ListingForm(request.POST)     
        if form.is_valid():
            # save form, add foreign key and commit
            #### FORM CLEAN DATA???
            #######
            form = form.save(commit=False)
            form.user_id = request.user.id
            form.save()
            return HttpResponseRedirect(reverse("index"))
           
    # method == GET
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })


# Form: new listing
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ("current_bid",)
        
        labels = {
            "current_bid": "Bid on this item $:"
        }


# Form: Add comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)
        
        widget = {
            "comment": forms.Textarea()
        }
        
        labels = {
            "comment": "Add your comment here!"
        }

   
# display listing, add/remove to watchlist
def listing(request, item_name):
    user = request.user
    listing = Listing.objects.get(title=item_name)    
    comments = Comment.objects.filter(listing_id=listing.id)
    message = None
    winner = None
    if request.method == "POST":
        # add/remove item -> watchlist
        if "watchlist" in request.POST:
            on_watchlist = Watchlist.objects.filter(user=user, listing=listing)
            
            # if on watchlist: remove item
            if on_watchlist:
                on_watchlist.delete()
                return HttpResponseRedirect(reverse("watchlist"))
            
            # add to watchlist       
            else:
                add_to_watchlist = Watchlist(user=user, listing=listing) 
                add_to_watchlist.save()
                return HttpResponseRedirect(reverse("watchlist"))
        
        # bid
        if "bid" in request.POST:
            form = BidForm(request.POST)
            form.fields["current_bid"].required = True
            if form.is_valid():                                       
                bid = form.cleaned_data["current_bid"]          
                max_bid = listing.start_bid
                highest_bid = listing.highest_bid
                message = "Your bid must be equal to or higher than the starting bid."  
                
                if listing.highest_bid > listing.start_bid:
                    max_bid = listing.highest_bid                    
                    message = "Your bid must be higher than the currently highest bid." 

                if (bid >= max_bid and highest_bid == 0) or (bid > max_bid and highest_bid > 0):
                    update_listing = Listing.objects.get(id=listing.id)
                    update_listing.highest_bid = bid
                    update_listing.save()
                    my_bid = Bid(user=user, listing=listing, current_bid=bid) 
                    my_bid.save()                    
                    return HttpResponseRedirect(reverse("watchlist"))                    

                #change pls       
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "form": BidForm(),
                        "form_2": CommentForm(),
                        "comments": comments,
                        "winner": winner,
                        "message": message
                    })
            
            
            #change pls       
            else:
                message = "You must enter a bid."
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": BidForm(),
                    "form_2": CommentForm(),
                    "comments": comments,
                    "winner": winner,
                    "message": message
                })

        if "close" in request.POST:
            if listing.user_id == user.id:
                listing = Listing.objects.get(id=listing.id)
                listing.closed = True
                listing.save()                
                if listing.highest_bid == 0:
                    listing.delete()
                pass

        if "comment" in request.POST:
            form_2 = CommentForm(request.POST)
            if form_2.is_valid():
                comment = form_2.cleaned_data["comment"]
                print(comment)
                new_comment = Comment(user=user, listing=listing, comment=comment)
                new_comment.save()
                pass
                
    # TO DO: if NOT logged in: redirect login form
    # inform winner of auction
    if listing.closed == True:
        winner = (Bid.objects.get(current_bid=listing.highest_bid, listing_id=listing.id)).user_id

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(),
        "form_2": CommentForm(),
        "comments": comments,
        "winner": winner,
        "message": message
    })     


# watchlist
@login_required(login_url='login')
def watchlist(request, **kwargs):
    user = request.user.id 
    if request.method == "POST":
        listing = kwargs.get("pk")
        on_watchlist = Watchlist.objects.filter(user=user, listing=listing)

        # if on watchlist: remove item
        if on_watchlist:
            on_watchlist.delete()
            return HttpResponseRedirect(reverse("watchlist"))
          
    # method == GET
    return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user=user)
    })


# categories
def categories():
    #TO DO
    pass

# Login
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
            
    # method == Get        
    else:
        return render(request, "auctions/login.html")

# Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# Register
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
    # method == Get   
    else:
        return render(request, "auctions/register.html")
