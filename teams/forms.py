from django import forms

from manager.models import Country, Team


class NewTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", widget=forms.TextInput(attrs={"class": "form-control"}))
    team_country = forms.ChoiceField(
        choices=[("selected", "Select Country")] + [(country.id, country.name) for country in Country.objects.all()], 
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Select Team Country"})
    )

    def clean_team_name(self):
        team_name = self.cleaned_data.get("team_name")
        if not team_name:
            raise forms.ValidationError("Team name is required!")
        if Team.objects.filter(name=team_name).exists():
            raise forms.ValidationError("Team name already exists!")
        return team_name

    def clean_team_country(self):
        team_id = self.cleaned_data.get("team_country")
        if team_id == "selected":
            raise forms.ValidationError("Select a country!")
        if not Country.objects.filter(id=int(team_id)).exists():
            raise forms.ValidationError("Select a country!")
        return team_id