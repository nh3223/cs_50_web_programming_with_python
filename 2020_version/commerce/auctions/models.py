from django.contrib.auth.models import AbstractUser
from django.db import models

from .forms import CreateListingForm

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=8)

class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

class Comment(models.Model):
    comment = models.CharField(max_length=512)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

class Category(models.Model):
    name = models.CharField(max_length=64)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='category')

class User(AbstractUser):
    listed_items = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_user')
    watched_items = models.ManytoManyField(Listing, on_delete=models.CASCADE, related_name='watching_users')