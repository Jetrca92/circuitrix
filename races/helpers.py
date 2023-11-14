import roman
from datetime import timedelta

from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from manager.models import Championship, Racetrack, Race
from races.constants import racetracks


@transaction.atomic
def create_races(championship):
    next_sunday = next_sunday_date()
    teams = championship.teams.all()
    for i, (code, racetrack) in enumerate(racetracks.items(), start=0):
        location = Racetrack.objects.get(name=racetrack["name"])
        date = next_sunday + timedelta(days=i * 7)
        r = Race(
            name=racetrack["name"] + " Grand Prix",
            date=date,
            location=location,
            laps=racetrack["total_laps"],
        )
        r.save()
        championship.races.add(r)
        championship.add_racetracks()
        championship.save()
        r.teams.set(teams)


@transaction.atomic
def create_championship(team, division, division_counter):
    name = f"{roman.toRoman(division)}.{division_counter}"
    if division == 1:
        name = "Circuitrix"
    championship = Championship(name=name, division=division)
    championship.save()
    create_races(championship)
    championship.teams.add(team)
    team.championship = championship
    team.save()


@transaction.atomic
def assign_championship(team):
    championship_schema = {
        # division: max number of championships in that division
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 16,
        6: 32,
        7: 64,
    }
    max_number_of_teams = 10
    highest_division = Championship.objects.aggregate(Max('division'))['division__max']
    
    if highest_division is None:
        # No divisions in the database, create the first championship
        create_championship(team, 1, 1)
    else:
        championships = Championship.objects.filter(division=highest_division)
        division_counter = championships.count()
        if division_counter == 0:
            # No championship yet
            create_championship(team, highest_division, 1)
        if championships.count() >= championship_schema[highest_division]:
            # If divisions full create div+1
            highest_division += 1
            division_counter = 0
        for championship in championships:
            # If place, add team
            if championship.teams.count() < max_number_of_teams:
                championship.teams.add(team)
                team.championship = championship
                team.save()
                add_team_to_upcoming_races(championship, team)
                return

        create_championship(team, highest_division, division_counter + 1)


def next_sunday_date():
    current_date = timezone.now()
    days_until_sunday = (6 - current_date.weekday() + 7) % 7
    next_sunday = current_date + timedelta(days=days_until_sunday)
    next_sunday_date = next_sunday.replace(hour=15, minute=0, second=0)
    return next_sunday_date


def add_team_to_upcoming_races(championship, team):
    upcoming_races = championship.races.filter(date__gt=timezone.now())
    if not upcoming_races:
        return
    for race in upcoming_races:
        race.teams.add(team)
        race.save()
    
