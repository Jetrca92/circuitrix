from django import forms

from manager.models import Country, Team, Driver


class NewTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", widget=forms.TextInput(attrs={"class": "form-control"}))
    team_country = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Select Team Country"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_country'].choices = self.get_country_choices()

    def get_country_choices(self):
        countries = Country.objects.all()
        choices = list(map(lambda country: (country.id, country.name), countries))
        return [("selected", "Select Country")] + choices

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
    

class EditCarNameForm(forms.Form):
    new_car_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), min_length=1, max_length=30)


class RaceOrdersForm(forms.Form):
    driver_1 = forms.ChoiceField(
        label="Driver 1",
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Select Driver"})
    )
    driver_2 = forms.ChoiceField(
        label="Driver 2",
        widget=forms.Select(attrs={"class": "form-select", "aria-label": "Select Driver"})
    )

    def __init__(self, team, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['driver_1'].choices = self.get_driver_choices(team)
        self.fields['driver_2'].choices = self.get_driver_choices(team)

    def get_driver_choices(self, team):
        drivers = Driver.objects.filter(team=team)
        choices = list(map(lambda driver: (driver.id, driver.surname), drivers))
        return [("selected", "Select Driver")] + choices