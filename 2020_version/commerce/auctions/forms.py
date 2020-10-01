from django import forms

class CreateListingForm(forms.Form)
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    opening_bid = forms.DecimalField()
    category = forms.CharField(max_length=64)
    user = forms.IntegerField(widget=forms.HiddenInput())