from django import forms

from manager.models import Manager
from messaging.models import Message

class NewMessageForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=Manager.objects.all(), 
        label="Recipient",
        empty_label="(Choose Recipient)", 
        widget=forms.Select(attrs={"class": "form-select", "id": "id_recipient"}),
        to_field_name="id",
    )
    subject = forms.CharField(
        label="Subject", 
        widget=forms.TextInput(attrs={"class": "form-control", "maxlength": "100"}),
    )
    content = forms.CharField(
        label="Content", 
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "16", "maxlength": "1000"}),
    )
    
    def __init__(self, *args, **kwargs):
        super(NewMessageForm, self).__init__(*args, **kwargs)
        # Modify the labels to use the 'name' field
        self.fields['recipient'].label_from_instance = lambda obj: obj.name if obj else self.fields['recipient'].empty_label
        

class DeleteMessageForm(forms.Form):
    delete_message_id = forms.CharField(widget=forms.HiddenInput())

    def clean_delete_message_id(self):
        message_id = self.cleaned_data.get("delete_message_id")
        if not message_id:
            raise forms.ValidationError("No Message ID!")
        return message_id
        
    def __init__(self, message_id, *args, **kwargs):
        super(DeleteMessageForm, self).__init__(*args, **kwargs)
        self.fields['delete_message_id'].initial = message_id