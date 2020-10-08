from django.forms import ModelForm, Form, HiddenInput, DecimalField, CharField, ModelChoiceField, Textarea
from auctions.models import Listing, Bid, Comment

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','starting_bid','category']

class BidForm(Form):
    bid = DecimalField()
    item = ModelChoiceField(queryset = Listing.objects.all(), widget=HiddenInput())
    
class CommentForm(Form):
    comment = CharField(widget=Textarea)
    item = ModelChoiceField(queryset = Listing.objects.all(), widget=HiddenInput())
