from django.db import transaction

from manager.models import Championship, Racetrack, Country


@transaction.atomic
def assign_championship(team):
    max_teams_in_championship = 10
    championships = Championship.objects.order_by('division')

    # Dictionary to keep track of the number of teams in each division
    division_count = {}

    for championship in championships:
        division = championship.division
        if division not in division_count:
            division_count[division] = championship.teams.count()

        if division_count[division] < max_teams_in_championship:
            championship.teams.add(team)
            team.championship = championship
            team.save()
            return
        
    # Check if there's a full championship with division=1
    if 1 in division_count and division_count[1] >= max_teams_in_championship:
        # Create a new championship with division=2
        new_championship = Championship(name=f"Division 2.{len(division_count) + 1}", division=2)
        new_championship.save()
        new_championship.teams.add(team)
        team.championship = new_championship
        team.save()
    else:
        # Create a new Circuitrix championship
        c = Championship(name="Circuitrix", division=1)
        c.save()
        c.teams.add(team)
        team.championship = c
        team.save()


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