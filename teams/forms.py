from django import forms

from manager.models import Country, Team


class NewTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", widget=forms.TextInput(attrs={"class": "form-control"}))
    team_country = forms.ChoiceField(
        choices=[("selected", "Select Country")],
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Select Team Country"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_country'].choices = self.get_country_choices()

    def get_country_choices(self):
        country_choices = [("selected", "Select Country")]
        countries = Country.objects.all()
        if countries.exists():
            country_choices.extend([(country.id, country.name) for country in countries])
        return country_choices

    def clean_team_name(self):
        team_name = self.cleaned_data.get("team_name")
        if not team_name:
            raise forms.ValidationError("Team name is required!")
        if Team.objects.filter(name=team_name).exists():
            raise forms.ValidationError("Team name already exists!")
        return team_name

    def clean_team_country(self):
        country_id = self.cleaned_data.get("team_country")
        if not country_id.isnumeric():
            raise forms.ValidationError("Select a country!")
        if not Country.objects.filter(id=int(country_id)).exists():
            raise forms.ValidationError("Select a country!")
        return country_id