from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auctions.forms import CreateListingForm, BidForm
from auctions.models import Listing, Bid, Comment, User


def index(request):
    listings = Listing.objects.all()
    for listing in listings:
        update_bid(listing)
    return render(request, "auctions/index.html", {'listings': listings})

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

@login_required
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid:
            new_listing = form.save()
            new_listing.lister = request.user
            new_listing.current_bid = new_listing.starting_bid
            new_listing.save()
            new_bid = Bid(bid = new_listing.starting_bid, bidder = new_listing.lister, item = new_listing)
            return render(request, 'auctions/<int:new_listing.id>.html', {'listing': new_listing})
        return render(request, 'auctions/create.html', {'form': form})                
    return render(request, 'auctions/create.html', {'form': CreateListingForm})

def listing(request, listing):
    form = BidForm(initial={'listing_id': listing.id, 'bidder': request.user})
    return render(request, 'auctions/<int:listing.id>.html', {'listing': listing, 'user': request.user, 'form': form})

def bid(request):
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid:
            new_bid = form.cleaned_data['bid']
            listing = Listing.objects.filter(id=form.cleaned_data['item'])
            prior_bid = listing.current_bid
            if new_bid > prior_bid:
                listing.current_bid = new_bid
            else:
                message = 'Bid must be higher than the current bid'
            form = BidForm(initial={'item': listing, 'bidder': request.user})
            return render(request, 'auctions/<int:listing.id>.html',
                            {'listing': listing, 'user': request.user, 'form': form, 'message': message})

def comment(request):
    pass


def update_bid(listing):
    listing.current_bid = Bid.objects.filter(item = listing).filter(Max(bid))
    listing.save()