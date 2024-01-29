import random
from datetime import timedelta
from unittest import mock
from unittest.mock import call, MagicMock

from django.test import TestCase
from django.utils import timezone

from manager.models import (
    Championship, Team, Manager, User, Racetrack, Race, Country, LeadDesigner, RaceMechanic,
    Car, Driver, RaceResult, Lap, Season, DriverPoints, TeamPoints
)
from races.constants import racetracks
from races.helpers import (
    assign_championship, add_team_to_upcoming_races, next_sunday_date,
    calculate_race_result, calculate_car_performance_rating,
    calculate_low_high_performance_rating, calculate_optimal_lap_time,
    get_race_drivers
)
from teams.constants import countries
from teams.helpers import generate_drivers, generate_car



class AssignChampionshipTestCase(TestCase):
    
    def test_assign_teams(self):
        # Create 1270 Users, Managers, and Teams for testing
        for i in range(1270):
            user = User.objects.create(username=f"user{i + 1}_test", password="password", email=f"user{i + 1}@gmail.com")
            manager = Manager.objects.create(name=f"Manager {i + 1}", user=user)
            team = Team.objects.create(name=f"Team {i + 1}", owner=manager)

        # Call the assign_championship function for each team
        for team in Team.objects.all():
            assign_championship(team)

        # Verify the results

        division1_championships = Championship.objects.filter(division=1)
        for championship in division1_championships:
            self.assertTrue(championship.teams.count() <= 10)

        division2_championships = Championship.objects.filter(division=2)
        for championship in division2_championships:
            self.assertTrue(championship.teams.count() <= 20)

        division3_championships = Championship.objects.filter(division=3)
        for championship in division3_championships:
            self.assertTrue(championship.teams.count() <= 40)

        division4_championships = Championship.objects.filter(division=4)
        for championship in division4_championships:
            self.assertTrue(championship.teams.count() <= 80)

        division5_championships = Championship.objects.filter(division=5)
        for championship in division5_championships:
            self.assertTrue(championship.teams.count() <= 160)

        division6_championships = Championship.objects.filter(division=6)
        for championship in division6_championships:
            self.assertTrue(championship.teams.count() <= 320)

        division7_championships = Championship.objects.filter(division=7)
        for championship in division7_championships:
            self.assertTrue(championship.teams.count() <= 640)


class AddTeamToUpcomingRacesTestCase(TestCase):
    def setUp(self):
        # Create a country
        self.country = Country.objects.create(name="Test Country", short_name="TC", logo_location="manager/flags/test.png")

        # Create a manager user
        self.user = User.objects.create_user(username="test_user", password="test_password", email="test@example.com")
        self.manager = Manager.objects.create(name="Test Manager", user=self.user)

        # Create a team with a lead designer, race mechanic, and car
        self.team = Team.objects.create(
            owner=self.manager,
            name="Test Team",
            location=self.country,
            total_fans=1000,
        )
        self.lead_designer = LeadDesigner.objects.create(name="Lead Designer", country=self.country, date_of_birth=timezone.now())
        self.race_mechanic = RaceMechanic.objects.create(name="Race Mechanic", country=self.country, date_of_birth=timezone.now())
        self.team.lead_designer = self.lead_designer
        self.team.race_mechanics.add(self.race_mechanic)
        self.team.save()

        self.car = Car.objects.create(name="Test Car", owner=self.team)

        # Create a driver
        self.driver = Driver.objects.create(
            name="Test Driver",
            country=self.country,
            date_of_birth=timezone.now(),
            skill_overall=80,
            skill_racecraft=70,
            skill_pace=90,
            skill_focus=80,
            skill_car_management=75,
            skill_feedback=85,
        )
        self.driver.team = self.team
        self.driver.save()

        # Create a racetrack
        self.racetrack = Racetrack.objects.create(
            name="Test Racetrack",
            location=self.country,
            image_location="manager/circuits/test.png",
            description="A test racetrack",
            lap_length_km=4.5,
            total_laps=50,
            straights=30.0,
            slow_corners=40.0,
            fast_corners=30.0,
        )

        # Create a championship with a race
        self.season = Season.objects.create(number=1, is_ongoing=True)
        self.championship = Championship.objects.create(name="Test Championship", season=self.season, division=1)
        self.championship.racetracks.add(self.racetrack)

        self.race = Race.objects.create(
            name="Test Race",
            season=self.season,
            date=timezone.now() + timedelta(days=7),
            location=self.racetrack,
            laps=10,
        )
        self.championship.races.add(self.race)

    def test_add_team_to_upcoming_races(self):
        # Add your team to upcoming races
        add_team_to_upcoming_races(self.championship, self.team)

        # Refresh the objects from the database
        self.race.refresh_from_db()
        self.team.refresh_from_db()

        # Ensure that the team has been added to the race
        self.assertIn(self.team, self.race.teams.all())

    def test_add_team_to_upcoming_races_multiple_races(self):
        # Create another race for testing
        another_race = Race.objects.create(
            name="Another Test Race",
            season=self.season,
            date=next_sunday_date() + timedelta(days=14),
            location=self.racetrack,
            laps=15,
        )
        self.championship.races.add(another_race)

        # Add your team to upcoming races
        add_team_to_upcoming_races(self.championship, self.team)

        # Refresh the objects from the database
        self.race.refresh_from_db()
        another_race.refresh_from_db()
        self.team.refresh_from_db()

        # Ensure that the team has been added to both races
        self.assertIn(self.team, self.race.teams.all())
        self.assertIn(self.team, another_race.teams.all())

    def test_add_team_to_upcoming_races_no_upcoming_races(self):
        # Move the race date to the past
        self.race.date = next_sunday_date() - timedelta(days=300)
        self.race.save()

        # Add your team to upcoming races
        add_team_to_upcoming_races(self.championship, self.team)

        # Refresh the objects from the database
        self.race.refresh_from_db()
        self.team.refresh_from_db()

        # Ensure that the team has not been added to the race
        self.assertNotIn(self.team, self.race.teams.all())


class CalculateRaceResultTestCase(TestCase):
    def setUp(self):
        # Create country and racetrack
        country = Country.objects.create(name="Italy", short_name="IT", logo_location="manager/flags/test.png")
        self.racetrack = Racetrack.objects.create(
            name="Test Monza Racetrack",
            location=country,
            image_location="manager/circuits/test.png",
            description="A test racetrack",
            lap_length_km=4.5,
            total_laps=50,
            straights=70.0,
            slow_corners=10.0,
            fast_corners=20.0,
        )
        # Generate teams
        for i in range(10):
            user = User.objects.create(username=f"user{i + 1}_test", password="password", email=f"user{i + 1}@gmail.com")
            manager = Manager.objects.create(name=f"Manager {i + 1}", user=user)
            team = Team.objects.create(name=f"Team {i + 1}", owner=manager, location=country)
            car = Car(
                owner=team,
                engine=random.randint(5, 20),
                gearbox=random.randint(5, 20),
                brakes=random.randint(5, 20),
                front_wing=random.randint(5, 20),
                suspension=random.randint(5, 20),
                rear_wing=random.randint(5, 20),
            )
            car.save()
            team.car = car
            team.save()
            generate_drivers(team)
        self.season = Season.objects.create(number=1, is_ongoing=True)
        self.race = Race.objects.create(
            name="Test Race",
            season=self.season,
            date=timezone.now(),
            location=self.racetrack,
            laps=1000,
        )
        self.race.teams.set(Team.objects.all())

    def test_car_function(self):
        drivers = Driver.objects.all()
        updated_drivers = calculate_race_result(self.race)
        sorted_updated_drivers = sorted(updated_drivers, key=lambda x: x['rank'])

        # After 1000 laps, cars should be sorted based on lap_time ascending
        for i in range(len(sorted_updated_drivers) - 1):
            current_driver = sorted_updated_drivers[i]
            next_driver = sorted_updated_drivers[i + 1]

            self.assertLessEqual(current_driver['lap_time'], next_driver['lap_time'])
            self.assertLessEqual(current_driver['rank'], next_driver['rank'])
            
        # Test object creation
        for driver in updated_drivers:
            result = RaceResult.objects.get(driver=Driver.objects.get(id=driver["driver_id"]))
            self.assertEqual(result.team, Team.objects.get(id=driver["team_id"]))
            self.assertEqual(result.race, self.race)

        for driver in updated_drivers:
            laps = Lap.objects.filter(race_result__driver=Driver.objects.get(id=driver['driver_id']))
            self.assertEqual(laps.count(), self.race.laps)

        for driver in updated_drivers:
            result = RaceResult.objects.get(driver=Driver.objects.get(id=driver["driver_id"]))
            self.assertEqual(result.position, driver["rank"])


class CalculateCarPerformanceRatingTestCase(TestCase):
    def setUp(self):

        # Create countries and teams
        for  country in countries.values():
            c, _created = Country.objects.get_or_create(
                short_name=country["short_name"],
                defaults={
                    "name": country["name"],
                    "logo_location": country["logo"],
                }
            )

        for i in range(10):
            user = User.objects.create(username=f"user{i + 1}_test", password="password", email=f"user{i + 1}@gmail.com")
            manager = Manager.objects.create(name=f"Manager {i + 1}", user=user)
            team = Team.objects.create(name=f"Team {i + 1}", owner=manager)
            car = Car(
                owner=team,
                engine=random.randint(5, 20),
                gearbox=random.randint(5, 20),
                brakes=random.randint(5, 20),
                front_wing=random.randint(5, 20),
                suspension=random.randint(5, 20),
                rear_wing=random.randint(5, 20),
            )
            car.save()
            team.car = car
            team.save()

        # Create Racetrack object
        for racetrack in racetracks.values():
            try:
                location = Country.objects.get(short_name=racetrack["location"])
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
            except Country.MultipleObjectsReturned:
                print(f"Multiple countries found for short_name '{racetrack['location']}'")

    def test_calculate_car_performance(self):
        for team in Team.objects.all():
            for racetrack in Racetrack.objects.all():   
                expected_result = (
                    (team.car.engine * racetrack.straights) +
                    (team.car.gearbox * ((racetrack.slow_corners + racetrack.fast_corners) / 2)) +
                    (team.car.brakes * racetrack.straights) +
                    (team.car.front_wing * racetrack.slow_corners) +
                    (team.car.suspension * racetrack.fast_corners) +
                    (team.car.rear_wing * racetrack.fast_corners)
                )
                actual_result = calculate_car_performance_rating(team.car, racetrack)

                self.assertEqual(expected_result, actual_result)

    def test_calculate_low_high_performance(self):
        for racetrack in Racetrack.objects.all():
            expected_result_min = (
                (5 * racetrack.straights) +
                (5 * ((racetrack.slow_corners + racetrack.fast_corners) / 2)) +
                (5 * racetrack.straights) +
                (5 * racetrack.slow_corners) +
                (5 * racetrack.fast_corners) +
                (5 * racetrack.fast_corners)
            )
            expected_result_max = (
                (20 * racetrack.straights) +
                (20 * ((racetrack.slow_corners + racetrack.fast_corners) / 2)) +
                (20 * racetrack.straights) +
                (20 * racetrack.slow_corners) +
                (20 * racetrack.fast_corners) +
                (20 * racetrack.fast_corners)
            )
            actual_result_min = calculate_low_high_performance_rating(5, racetrack)
            actual_result_max = calculate_low_high_performance_rating(20, racetrack)

            self.assertEqual(expected_result_min, actual_result_min)
            self.assertEqual(expected_result_max, actual_result_max)

    @mock.patch('races.helpers.calculate_car_performance_rating', return_value=10)
    @mock.patch('races.helpers.calculate_low_high_performance_rating', side_effect=lambda number, racetrack: number)
    def test_calculate_optimal_lap_time(self, lhpr, cpr):
        car = Car.objects.first()
        racetrack = Racetrack.objects.first()

        self.assertEqual(84, calculate_optimal_lap_time(car, racetrack))

        lhpr.assert_has_calls([
            call(5, racetrack,),
            call(20, racetrack,),
        ])

        cpr.assert_called_with(car, racetrack)
                    

class GetRaceResultTestCase(TestCase):
    def setUp(self):
        self.season = Season.objects.create(number=1)
        for country in countries.values():
            c, _created = Country.objects.get_or_create(
                short_name=country["short_name"],
                defaults={
                    "name": country["name"],
                    "logo_location": country["logo"],
                }
            )
        self.racetrack = Racetrack.objects.create(
            name="Test racetrack",
            location = Country.objects.filter(short_name="IT").first(),
            description = "test",
            lap_length_km = 5,
            total_laps = 65,
            straights = 33,
            slow_corners = 33,
            fast_corners = 34,
        )
        for i in range(10):
            user = User.objects.create(username=f"user{i + 1}_test", password="password", email=f"user{i + 1}@gmail.com")
            manager = Manager.objects.create(name=f"Manager {i + 1}", user=user)
            team = Team.objects.create(name=f"Team {i + 1}", owner=manager, location=Country.objects.filter(short_name="IT").first())
            self.race = Race.objects.create(
                name="Test Race",
                season=self.season,
                date=timezone.now(),
                location=self.racetrack,
                laps=1,
            )
            generate_drivers(team)

    def test_driver_list_no_race_orders(self):
        drivers = get_race_drivers(self.race)
        expected_drivers = [driver for team in self.race.teams.all() for driver in team.drivers.all()]
        self.assertEqual(drivers, expected_drivers)


class TestPointsMethods(TestCase):

    def setUp(self):
         # Create team and championship
        self.country = Country.objects.create(name="Test Country", short_name="IT", logo_location="manager/flags/test.png")
        self.user = User.objects.create_user(username="test_user", password="test_password", email="test@example.com")
        self.manager = Manager.objects.create(name="Test Manager", user=self.user)
        self.team = Team.objects.create(
            owner=self.manager,
            name="Test Team",
            location=self.country,
            total_fans=1000,
        )
        generate_drivers(self.team)
        generate_car(self.team)
        self.season = Season.objects.create(number=1)
        self.championship = Championship.objects.create(
            name="test123",
            season=self.season,
        )
        self.racetrack = Racetrack.objects.create(
            name="Test racetrack",
            location = self.country,
            description = "test",
            lap_length_km = 5,
            total_laps = 65,
            straights = 33,
            slow_corners = 33,
            fast_corners = 34,
        )
        self.race = Race.objects.create(
            name="test_race",
            season=self.season,
            championship=self.championship,
            date=timezone.now(),
            location=self.racetrack,
            laps=65,
        )
        self.race.teams.add(self.team)
        self.race.save()
            

    def test_team_points_add_points_method(self):
        team_points, _created = TeamPoints.objects.get_or_create(team=self.team, championship=self.race.championship)
        self.assertEqual(team_points.points, 0)
        team_points.add_points(5)
        self.assertEqual(team_points.points, 5)

    def test_driver_points_add_points_method(self):
        driver = Driver.objects.filter(team=self.team).first()
        driver_points, _created = DriverPoints.objects.get_or_create(driver=driver, championship=self.race.championship)
        driver_points.add_points(7)
        self.assertEqual(driver_points.points, 7)

    def test_award_points_method(self):
        calculate_race_result(self.race)
        winner = RaceResult.objects.get(race=self.race, team=self.team, position=1)
        self.assertEqual(winner.position, 1)
        self.race.championship.award_points(self.race)
        winner_points = DriverPoints.objects.get(championship=self.race.championship, driver=winner.driver)
        self.assertEqual(winner_points.points, 25)
        
        
        