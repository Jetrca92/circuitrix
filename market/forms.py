from django import forms


class FireDriverForm(forms.Form):
    confirmation = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))


class ListDriverForm(forms.Form):
    confirmation = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    price = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))


class DriverBidForm(forms.Form):
    amount = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
