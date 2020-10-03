from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
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
            new_bid.save()
            return render(request, 'auctions/listing.html', {'listing': new_listing})
        return render(request, 'auctions/create.html', {'form': form})                
    return render(request, 'auctions/create.html', {'form': CreateListingForm})

def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, 'auctions/listing.html', {'listing': listing, 'user': request.user, 'bidform': BidForm(initial={'bid': listing.current_bid, 'item': listing})})

def bid(request):
    if request.method == 'POST':
        bidform = BidForm(request.POST)
        if bidform.is_valid():
            bid = bidform.cleaned_data['bid']
            listing = bidform.cleaned_data['item']
            prior_bid = listing.current_bid
            if bid > prior_bid:
                listing.current_bid = bid
                new_bid = Bid(bid=bid, bidder = request.user, item = listing)
                new_bid.save()
                listing.save()
                return render(request, 'auctions/listing.html', {'listing': listing, 'user': request.user, 'bidform': BidForm(initial={'bid': listing.current_bid, 'item': listing})})
            else:
                message = 'Bid must be higher than the current bid'
                return render(request, 'auctions/listing.html', {'message': message, 'listing': listing, 'user': request.user, 'bidform': BidForm(initial={'bid': listing.current_bid, 'item': listing}), 'message': message})
    return redirect(reverse('listing'))
    
def comment(request):
    pass


def update_bid(listing):
    bids = Bid.objects.filter(item=listing).values_list('bid', flat=True)
    listing.current_bid = max(bids)
    listing.save()