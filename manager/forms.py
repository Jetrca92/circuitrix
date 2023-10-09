from django import forms

from manager.models import Country


class NewTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    team_country = forms.ChoiceField(
        choices=[("selected", "Select Country")] + [(country.id, country.name) for country in Country.objects.all()], 
        widget=forms.Select(attrs={'class': 'form-select', 'aria-label': 'Select Team Country'}))
    
