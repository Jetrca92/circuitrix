from django import forms

from market.models import Bid, DriverListing


class FireDriverForm(forms.Form):
    confirmation = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))


class ListDriverForm(forms.Form):
    confirmation = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    price = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))


class DriverBidForm(forms.Form):
    driver_listing = forms.ModelChoiceField(
        queryset=DriverListing.objects.all(),
        widget=forms.HiddenInput(),
    )
    amount = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        driver_listing = self.cleaned_data.get('driver_listing')
        existing_bids = Bid.objects.filter(driver_listing=driver_listing)
        highest_bid = existing_bids.order_by("-amount").first()
        if highest_bid is not None and amount <= highest_bid.amount:
            raise forms.ValidationError("Bid amount must be higher than the highest bid!")
        if amount <= driver_listing.price:
            raise forms.ValidationError("Bid amount must be higher than the price!")
        return amount


