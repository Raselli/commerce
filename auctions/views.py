from asyncio.windows_events import NULL
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment, Category

# Home
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.select_related()
    })

# Form: new listing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "start_bid", "img_url", "category")
            
        widgets = {
            "description": forms.Textarea(),
            "category": forms.Select()
        }
        
        labels = {
            "title": "Title of listing item",
            "Description": "Description of listing item",
            "start_bid": "Staring Bid $:",
            "img_url": "Add an URL of your listing:",
            "category": "Choose a category."
        }
        
        
#  create new listing
@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        
        # save form, add foreign key and commit            
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user.id
            form.save()
            return HttpResponseRedirect(f"listing/{form.title}")
        
        # invalid form data
        else:
            return render(request, "auctions/create_listing.html", {
                "form": ListingForm(),
                "message": "Invalid input."
            })             

    # method == GET
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })


# Form: new listing
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["current_bid"]
        
        labels = {
            "current_bid": "Place your bid:"
        }


# Form: Add comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        
        widgets = {
            "comment": forms.Textarea(attrs={"rows":3, "cols":10})
        }
        
        labels = {
            "comment": "Add your comment here!"
        }

   
# display listing page
def listing(request, item_name):
    
    # Query listing
    try: 
        listing = Listing.objects.prefetch_related().get(title=item_name)
    except:
        raise Http404("Listing does not exist.")

    user = request.user
    comments = Comment.objects.filter(listing_id=listing.id)
    bid_count = Bid.objects.filter(listing_id=listing.id).count()

    # Query current highest bidder
    try:
        highest_bidder = Bid.objects.get(current_bid=listing.highest_bid, listing_id=listing.id)
    except:
        highest_bidder = None
  
    # Query watchlist
    try:
        on_watchlist = Watchlist.objects.filter(user=user, listing=listing).first()         
    except:
        on_watchlist = None

    # method == POST: Login required
    if request.method == "POST":

        # Add/remove item from watchlist
        if "watchlist" in request.POST:
            if on_watchlist:
                on_watchlist.delete()     
            else:
                add_to_watchlist = Watchlist(user=user, listing=listing) 
                add_to_watchlist.save()
            return HttpResponseRedirect(f"{listing.title}") 
        
        # Bid on listing-item (login req.)
        if "bid" in request.POST:
            form = BidForm(request.POST)
            form.fields["current_bid"].required = True
            if form.is_valid():                                       
                bid = form.cleaned_data["current_bid"]
                
                # Invalid bid
                if bid < 0:                 
                    message = "You must enter a valid bid."
                    
                # Invalid bid at starting_bid
                elif listing.highest_bid == 0 and bid < listing.start_bid: 
                    message = "Your bid must be atleast equal to the starting bid."                 

                # Invalid bid at current_bid
                elif listing.highest_bid > 0 and bid <= listing.highest_bid:
                    message = "Your bid must be higher than the current bid."                     
                    
                # Accept bid  
                else:
                    update_listing = Listing.objects.get(id=listing.id)
                    update_listing.highest_bid = bid
                    update_listing.save()
                    my_bid = Bid(user=user, listing=listing, current_bid=bid) 
                    my_bid.save()
                    return HttpResponseRedirect(f"{listing.title}")                   

            # invalid bid-form data
            else:
                message = "You must enter a valid bid."
            
            # render listing with message
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "form": BidForm(),
                "form_2": CommentForm(),
                "comments": comments,
                "message": message,
                "leading_bid": highest_bidder,
                "count": bid_count,
                "watchlist": on_watchlist
            })                     

        # Close active auction (owner only)
        if "close" in request.POST:
            if listing.user_id == user.id:
                listing = Listing.objects.get(id=listing.id)
                listing.closed = True
                listing.save()
                return HttpResponseRedirect(f"{listing.title}")                

        # Add comment to listing
        if "comment" in request.POST:
            form_2 = CommentForm(request.POST)
            if form_2.is_valid():
                comment = form_2.cleaned_data["comment"]              
                new_comment = Comment(user=user, listing=listing, comment=comment)
                new_comment.save()
            return HttpResponseRedirect(f"{listing.title}")  

    # method == GET
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(),
        "form_2": CommentForm(),
        "comments": comments,
        "leading_bid": highest_bidder,
        "count": bid_count,
        "watchlist": on_watchlist
    })        


# watchlist
@login_required(login_url='login')
def watchlist(request, **kwargs):
    user = request.user.id
    
    # remove item from watchlist
    if request.method == "POST":
        listing = kwargs["pk"]
        try:            
            on_watchlist = Watchlist.objects.get(user=user, listing=listing)
            on_watchlist.delete()
            return HttpResponseRedirect(reverse("watchlist"))
        except:
            raise Http404("Watchlist-item does not exist.")
        
    # method == GET
    else:         
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(user=user)
        })


# categories
def categories(request, **kwargs):
    if kwargs:
        # render category "unlisted"
        if kwargs["cat_name"] == "unlisted":
            return render(request, "auctions/categories.html", {
                "categories": Category.objects.all(),
                "active_cat": "unlisted",
                "listings": Listing.objects.filter(category_id=None)
            })                   

        # render category (excluding": "unlisted")
        try:
            active_cat = kwargs["cat_name"]
            cat_id = Category.objects.get(category=active_cat).id
            return render(request, "auctions/categories.html", {
                "categories": Category.objects.all(),
                "active_cat": active_cat,
                "listings": Listing.objects.filter(category_id=cat_id)
            })               
            
        except:
            raise Http404("Category does not exist.")

    # method == GET
    else:
        return render(request, "auctions/categories.html", {
            "categories": Category.objects.all()
        })


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
