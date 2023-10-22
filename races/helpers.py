from manager.models import Championship

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