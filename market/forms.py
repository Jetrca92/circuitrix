from django import forms


class SellDriverForm(forms.Form):
    confirmation = forms.BooleanField(required=True)
    