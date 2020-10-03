from django.forms import ModelForm, Form, IntegerField, HiddenInput, DecimalField, ModelChoiceField
from auctions.models import Listing, Bid, Comment

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','starting_bid','category']

class BidForm(Form):
    bid = DecimalField()
    item = ModelChoiceField(queryset = Listing.objects.all())
    
class CommentForm(ModelForm):
    class Meta:
        pass