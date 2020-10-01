from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=64)
    current_bid = models.DecimalField(max_digits=8, decimal_places=2)
    active = models.BooleanField(default=True)
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_items', default=None)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_items', default=None)

    def __str__(self):
        return f'{self.title}: {self.description}\nCurrent Bid: {self.current_bid}'

class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

class Comment(models.Model):
    comment = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')

