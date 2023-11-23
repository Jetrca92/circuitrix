import roman
import random
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
    

def calculate_car_performance_rating(car, racetrack):
    performance = (car.engine * racetrack.straights) + \
        (car.gearbox * ((racetrack.slow_corners + racetrack.fast_corners) / 2)) + \
        (car.brakes * racetrack.straights) + \
        (car.front_wing * racetrack.slow_corners) + \
        (car.suspension * racetrack.fast_corners) + \
        (car.rear_wing * racetrack.fast_corners)
    return performance


def calculate_low_high_performance_rating(low_high_rating_number, racetrack):
    performance = (low_high_rating_number * racetrack.straights) + \
        (low_high_rating_number * ((racetrack.slow_corners + racetrack.fast_corners) / 2)) + \
        (low_high_rating_number * racetrack.straights) + \
        (low_high_rating_number * racetrack.slow_corners) + \
        (low_high_rating_number * racetrack.fast_corners) + \
        (low_high_rating_number * racetrack.fast_corners)
    return performance


def calculate_optimal_lap_time(car, racetrack) -> int:
    rating_low = calculate_low_high_performance_rating(5, racetrack)
    rating_high = calculate_low_high_performance_rating(20, racetrack)
    rating = calculate_car_performance_rating(car, racetrack)
    
    # Get max, min constant
    constant_low = racetracks[racetrack.location.short_name]["worst_benchmark_time"] * rating_low
    constant_high = racetracks[racetrack.location.short_name]["best_benchmark_time"] * rating_high
    
    # Linear interpolation to determine the constant for the specific rating
    constant = constant_low + ((rating - rating_low) / (rating_high - rating_low)) * (constant_high - constant_low)
    
    lap_time = int(constant / rating)
    return lap_time


def calculate_race_result(teams, racetrack):
    cars = [team.car for team in teams]
    laps = 10
    positions = {}

    for lap in range(laps):
        lap_times = {f"{car.owner.name}": calculate_optimal_lap_time(car, racetrack) * random.uniform(1.0, 1.0) for car in cars}

        # Convert dictionary items to a list of tuples for easier iteration
        team_lap_times = list(lap_times.items())
        
        # Find the pair with the biggest time difference
        biggest_lap_diff = 0
        teams_with_biggest_diff = None
        
        # Iterate through the list to find lap time differences
        for i in range(len(team_lap_times) - 1):
            team_1, lap_time_1 = team_lap_times[i]
            team_2, lap_time_2 = team_lap_times[i + 1]

            lap_time_diff = lap_time_2 - lap_time_1
            if lap_time_diff < biggest_lap_diff and lap_time_diff < 0:
                biggest_lap_diff = lap_time_diff
                teams_with_biggest_diff = (team_1, team_2)
        print(f"Lap {lap + 1} lap times: {lap_times}")
        if teams_with_biggest_diff:
            print(f"Difference between {teams_with_biggest_diff}: {biggest_lap_diff:.2f} seconds")
            # Swap the positions of the teams in the cars list
            team_1_index = [i for i, team in enumerate(teams) if team.car.owner.name == teams_with_biggest_diff[0]][0]
            team_2_index = [i for i, team in enumerate(teams) if team.car.owner.name == teams_with_biggest_diff[1]][0]

            cars[team_1_index], cars[team_2_index] = cars[team_2_index], cars[team_1_index]
            print(f"Swapping {teams_with_biggest_diff[0]} and {teams_with_biggest_diff[1]}")

        positions[lap + 1] = [car.owner.name for car in cars]
        

    print(positions)
    return positions


def simple_calculation():
    teams = [
        {
            'name': 'McLaren', 
            'rating': 90, 
            'rank': 1
        },
        {
            'name': 'Ferarri', 
            'rating': 85, 
            'rank': 2
        },
        {
            'name': 'RedBull', 
            'rating': 100, 
            'rank': 3
        },
        {
            'name': 'AlphaTauri', 
            'rating': 65, 
            'rank': 4
        },
        {
            'name': 'Mercedes', 
            'rating': 89, 
            'rank': 5
        },
        {
            'name': 'Alpine', 
            'rating': 68, 
            'rank': 6
        },
        {
            'name': 'Haas', 
            'rating': 65, 
            'rank': 7
        },
        {
            'name': 'AlfaRomeo', 
            'rating': 64, 
            'rank': 8
        },
        {
            'name': 'AstonMartin', 
            'rating': 83, 
            'rank': 9
        },
        {
            'name': 'Williams', 
            'rating': 76, 
            'rank': 10
        }]

    laps = 5
    
    for lap in range(laps):
        max_diff = 0
        teams_with_max_diff = None
        teams = sorted(teams, key=lambda x: x["rank"])
        for i in range(len(teams) - 1):
            team_1 = teams[i]
            team_2 = teams[i + 1]

            rating_diff = team_1["rating"] - team_2["rating"]

            if rating_diff < max_diff and rating_diff < 0:
                max_diff = rating_diff
                teams_with_max_diff = (team_1, team_2)

        if teams_with_max_diff:
            team_1_index = teams.index(teams_with_max_diff[0])
            team_2_index = teams.index(teams_with_max_diff[1])

            teams[team_1_index]["rank"], teams[team_2_index]["rank"] = teams[team_2_index]["rank"], teams[team_1_index]["rank"]
        teams = sorted(teams, key=lambda x: x['rank'])
        print("Maximum Rating Difference:", max_diff)
        print("Teams with the highest rating difference:", teams_with_max_diff)
        print("Updated Teams:", teams)


