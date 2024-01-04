from django import forms

from messaging.models import Message

class NewMessageForm(forms.Form):
    receiver_id = forms.CharField(label="Receiver (id)", widget=forms.TextInput(attrs={"class": "form-control", "maxlength": "100", "id": "id_receiver"}))
    subject = forms.CharField(label="Subject", widget=forms.TextInput(attrs={"class": "form-control", "maxlength": "100"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "form-control", "rows": "16", "maxlength": "1000"}))

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if not content:
            raise forms.ValidationError("You can't send an empty message!")
        return content
    
    def clean_receiver(self):
        receiver = self.cleaned_data.get("receiver")
        if not receiver:
            raise forms.ValidationError("Please provide the receiver's ID")