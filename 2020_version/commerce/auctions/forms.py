from django.forms import ModelForm, IntegerField, HiddenInput
from auctions.models import Listing, Bid

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','opening_bid','category']

class BidForm(ModelForm):
    item = IntegerField(widget=HiddenInput())
    bidder = IntegerField(widget=HiddenInput())
    class Meta:
        model = Bid
        fields = ['bid','item','bidder']

class CommentForm(ModelForm):
    class Meta:
        model = Comment