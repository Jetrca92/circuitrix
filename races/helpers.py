import roman

from django.db import transaction
from django.db.models import Max

from manager.models import Championship, Racetrack, Country


@transaction.atomic
def assign_championship(team):
    max_number_of_teams = 10
    highest_division = Championship.objects.aggregate(Max('division'))['division__max']
    championship_schema = {
        # division: max number of championships in that division
        2: 2,
        3: 4,
        4: 8,
        5: 16,
        6: 32,
        7: 64,
    }

    def create_championship(division, division_counter):
        name = f"{roman.toRoman(division)}.{division_counter + 1}"
        if division_counter == 0 and division == 1:
            name = "Circuitrix"
        championship = Championship(name=name, division=division)
        championship.save()
        championship.teams.add(team)
        team.championship = championship
        team.save()

    if highest_division is None:
        # No divisions in the database, create the first championship
        create_championship(1, 0)
    else:
        if highest_division == 1:
            # Division 1 exists, if not full add team
            championship = Championship.objects.get(division=highest_division)
            if championship.teams.count() >= max_number_of_teams:
                highest_division += 1
            else:
                championship.teams.add(team)
                team.championship = championship
                team.save()
                return

        championships = Championship.objects.filter(division=highest_division)
        division_counter = championships.count()
        if division_counter == 0:
            # No championship yet
            create_championship(highest_division, 0)
        if championships.count() >= championship_schema[highest_division]:
            # If divisions full create div+1
            highest_division += 1
        for championship in championships:
            # If place, add team
            if championship.teams.count() < max_number_of_teams:
                championship.teams.add(team)
                team.championship = championship
                team.save()
                return

        create_championship(highest_division, division_counter)

@transaction.atomic
def create_racetracks(racetracks):
    for code, racetrack in racetracks.items():
        location=Country.objects.get(short_name=racetrack["location"])
        r = Racetrack(
            name=racetrack["name"],
            location=location,
            image_location=racetrack["image_location"],
            description=racetrack["description"],
            lap_length_km=racetrack["lap_length_km"],
            total_laps=racetrack["total_laps"],
            straights=racetrack["straights"],
            slow_corners=racetrack["slow_corners"],
            fast_corners=racetrack["fast_corners"],
        )
        r.save()


@transaction.atomic
def create_countries(countries):
    for code, country in countries.items():
        c = Country(
            name=country["name"],
            short_name=country["short_name"],
            logo_location=country["logo"],
        )
        c.save()