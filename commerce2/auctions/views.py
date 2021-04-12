from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction_listing, Bid




##class form
class NewListingForm(forms.Form):
    title = forms.CharField(label="New listing title")
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}),label="Listing description")
    bid = forms.FloatField(label="Starting bid")
    image = forms.URLField(label="Listing's image URL")


def index(request):
    return render(request, "auctions/index.html", {
    "listings": Auction_listing.objects.all(),
    "bids": Bid.objects.all()
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
            f = Auction_listing(title=form.cleaned_data['title'], description= form.cleaned_data['description'], image = form.cleaned_data['image'])
            f.save()
            g = Bid(bid= form.cleaned_data['bid'])
            g.save()
            return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
        })


