import roman
import random
from datetime import timedelta

from django.db import transaction
from django.db.models import Max
from django.utils import timezone

from manager.models import Championship, Racetrack, Race, RaceResult, Lap, Team, Driver
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


def calculate_race_result(drivers, race):
    drivers = [
        {
            "team_name": driver.team.name,
            "team_id": driver.team.id,
            "rank": i + 1,
            "lap_time": calculate_optimal_lap_time(driver.team.car, race.location),
            "driver_id": driver.id
        }
        for i, (driver) in enumerate(drivers, start=0)
    ]
    laps = race.laps
    for driver in drivers:
        result = RaceResult(
            race=race,
            team=Team.objects.get(id=driver["team_id"]),
            driver=Driver.objects.get(id=driver["driver_id"]),
        )
        result.save()
    for i in range(laps):
        max_diff = 0
        drivers_with_max_diff = None
        lap_number = i + 1
        sorted_drivers = sorted(drivers, key=lambda x: x["rank"])
        for i in range(len(sorted_drivers) - 1):
            # Get max difference between adjacent cars
            driver_1 = sorted_drivers[i]
            driver_2 = sorted_drivers[i + 1]

            rating_diff = driver_2["lap_time"] - driver_1["lap_time"]

            if rating_diff < max_diff and rating_diff < 0:
                max_diff = rating_diff
                drivers_with_max_diff = (driver_1, driver_2)

            # Add result to model
            lap = Lap(
                time=driver_1["lap_time"],
                lap_number=lap_number,
                race_result=RaceResult.objects.get(driver=Driver.objects.get(id=driver_1["driver_id"]))
            )
            lap.save()

        if drivers_with_max_diff:
            driver_1_index = drivers.index(drivers_with_max_diff[0])
            driver_2_index = drivers.index(drivers_with_max_diff[1])

            sorted_drivers[driver_1_index]["rank"], sorted_drivers[driver_2_index]["rank"] = sorted_drivers[driver_2_index]["rank"], sorted_drivers[driver_1_index]["rank"]
        sorted_drivers = sorted(sorted_drivers, key=lambda x: x['rank'])

        print(f"Lap number: {lap_number}")
        print("Maximum Time Difference:", max_diff)
        print("Drivers with the highest Time difference:", drivers_with_max_diff)
        print("Updated Drivers:", sorted_drivers)
