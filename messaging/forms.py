from django import forms

from messaging.models import Message

class NewMessageForm(forms.Form):
    subject = forms.CharField(label="Subject", widget=forms.TextInput(attrs={"class": "form-control", "maxlength": "100"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "form-control", "rows": "16", "maxlength": "1000"}))

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content == "":
            raise forms.ValidationError("You can't send an empty message!")
        return content