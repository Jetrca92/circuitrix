import roman

from django.db import transaction
from django.db.models import Max

from manager.models import Championship


@transaction.atomic
def assign_championship(team):
    max_number_of_teams = 10
    highest_division = Championship.objects.aggregate(Max('division'))['division__max']
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

    def create_championship(division, division_counter):
        name = f"{roman.toRoman(division)}.{division_counter}"
        if division == 1:
            name = "Circuitrix"
        championship = Championship(name=name, division=division)
        championship.save()
        championship.teams.add(team)
        team.championship = championship
        team.save()

    if highest_division is None:
        # No divisions in the database, create the first championship
        create_championship(1, 1)
    else:
        championships = Championship.objects.filter(division=highest_division)
        division_counter = championships.count()
        if division_counter == 0:
            # No championship yet
            create_championship(highest_division, 1)
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
                return

        create_championship(highest_division, division_counter + 1)