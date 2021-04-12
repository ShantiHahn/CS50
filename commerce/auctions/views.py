from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction_listing, Bid, Comment

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


##class form
class NewListingForm(forms.Form):
    title = forms.CharField(label="New listing title")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}),label="Listing description")
    bid = forms.FloatField(label="Starting bid")
    image = forms.URLField(label="Listing's image URL",required=False)
    category = forms.CharField(label="Category")
    # class Meta:
    #     model = Auction_listing
    #     exclude = ['user', ]


# def bid_validator(value, initial):
#     if value <= initial : 
#         raise ValidationError(
#             _('%(value)s is not higuer than previous bids'),
#             params={'value': value},
#         )

class BiddingForm(forms.Form):
    topping_bid = forms.FloatField(label="Top this bid !")


class WatchListForm(forms.Form):

    watchlist = forms.BooleanField(label="Add this listing to your Watchlist ?")

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment this listing",widget =forms.Textarea(attrs={"rows":5, "cols":20}))

class CloseForm(forms.Form):

    close = forms.BooleanField(label="Turn this on/off")


####utils



def index(request):
    #data
    listings = Auction_listing.objects.filter(active=True)
    bids = Bid.objects.all()
    categories = []
    max_bids = {}
    for i in listings:
        max_bid = bids.filter(auction=i).latest('bid').bid
        max_bids[i] = max_bid
    for i in listings: 
        categories.append(i.category)
    print(max_bids)
    return render(request, "auctions/index.html", {
    "max_bids": max_bids,
    "listings": listings,
    "bids": bids,
    "categories" : categories
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


def create_listing(request):

    if request.method == 'POST':

        form = NewListingForm(request.POST)

        if form.is_valid():
            f = Auction_listing(title=form.cleaned_data['title'], description= form.cleaned_data['description'], image = form.cleaned_data['image'], category=form.cleaned_data['category'], seller= request.user)
            f.save()
            g = Bid(bid= form.cleaned_data['bid'],auction=f, user= request.user)
            g.save()
            return HttpResponseRedirect(reverse("index"))

        
        else:
            form = NewListingForm()
            return render(request, "auctions/create_listing.html", {
                "form": NewListingForm()
            })
    

    else:

        form = NewListingForm()
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
        })

def listing(request, listing_id):
    #data
    listing = Auction_listing.objects.get(id = listing_id)
    bids = Bid.objects.filter(auction= listing)
    comments = Comment.objects.filter(auction=listing)
    high_bid = bids.latest("bid")

    #forms
    bidding_form = BiddingForm(request.POST or None, request.FILES or None)
    comment_form = CommentForm(request.POST)
    watchlist = WatchListForm(request.POST)
    closeform = CloseForm(request.POST)
    #user
    user = User.objects.get(username=request.user.username)

    #messages

    
    if request.method == 'POST':
        
        if watchlist.is_valid():
            #if watchlist is True:
                user.watchlist.add(listing)
                

                return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        if comment_form.is_valid():
            newcomment = Comment(auction= listing, comment=comment_form.cleaned_data['comment'], user= request.user)
            newcomment.save()

            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

        if bidding_form.is_valid():
            newbid = Bid(bid=bidding_form.cleaned_data['topping_bid'], auction = listing, user= request.user)

            if newbid.bid > bids.latest('bid').bid :
                succes_message = "bid successful"
                failure_message=""
                print(succes_message)
                newbid.save()
            else:
                succes_message = ""
                failure_message = "bid failed, bid must be higher than previous bids"
                print(failure_message)
            return render(request, "auctions/listing.html", {
                "succes_message": succes_message,
                "failure_message": failure_message,
                "listing" : listing,
                "listing_id": listing.id,
                "bids" : bids,
                "high_bid": high_bid,
                "comments": comments,
                "bidding_form" : bidding_form,
                "comment_form": comment_form,
                "closeform": closeform,
                "watchlist": watchlist,
                "user": user
            } )
        if closeform.is_valid():
            listing.active = not listing.active 
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "listing_id": listing.id,
        "bids" : bids,
        "high_bid": high_bid,
        "comments": comments,
        "bidding_form" : bidding_form,
        "comment_form": comment_form,
        "closeform": closeform,
        "watchlist": watchlist,
        "user": user
    } )

def test(request):
    

    return render(request,"auctions/test.html", {
    "listings": Auction_listing.objects.all(),
    "bids": Bid.objects.all()
    })

def watchlist(request):
    #data
    watchlist = request.user.watchlist.all()
    bids = []
    for i in watchlist :
        bids.append(Bid.objects.filter(auction = i))

    if request.method == 'POST' :
        closeform = CloseForm[request.POST]

        if closeform.is_valid():
            print('hello')
            ##watchlist.remove(watchlist[i])

        return HttpResponseRedirect(reverse("watchlist"))

    else:
        closeform = CloseForm    
        
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist,
            "bids" : bids
        })

#test for watchlist
def watchtest(request):
    watchtest = request.user.watchlist.all()    
    return render(request, "auctions/watchtest.html", {
        "watchtest": watchtest
    })

#display active items by categories
def category_search(request, category):
    listings_category = Auction_listing.objects.filter(category=category)
    print(listings_category)

    return render(request, "auctions/category_search.html", {
        "listings_category": listings_category,
        "category": category
    })

#display listing posted by the user
def seller(request):
 
    if request.method == 'POST':

        listings = Auction_listing.objects.filter(seller = request.user)
        active_listings = []
        closed_listings = []
        closeform = CloseForm(request.POST)
        for l in listings:
            if l.active:
                active_listings.append(l)
            else:
                closed_listings.append(l)

        if closeform.is_valid():
            f = Auction_listing.objects.get(id=closeform.cleaned_data['id'])
            f.active = False
            f.save()
            return HttpResponseRedirect(reverse("seller"))
        
        else :
            return HttpResponseRedirect(reverse("seller"))

    else:
        listings = Auction_listing.objects.filter(seller = request.user)
        active_listings = []
        closed_listings = []
        closeform = CloseForm()
        for l in listings:
            if l.active:
                active_listings.append(l)
            else:
                closed_listings.append(l)
    
        return render(request, "auctions/seller.html", {
        "active_listings": active_listings,
        "closed_listings": closed_listings,
        "closeform": closeform
        })
