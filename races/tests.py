from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from manager.models import Championship, Team, Manager, User, Racetrack, Race, Country, LeadDesigner, RaceMechanic, Car, Driver
from races.helpers import assign_championship, add_team_to_upcoming_races, next_sunday_date  

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

        # Add more assertions as needed to validate the results.
        for i in Championship.objects.all():
            print(i.__dict__, i.teams.count())


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
        self.championship = Championship.objects.create(name="Test Championship", division=1)
        self.championship.racetracks.add(self.racetrack)

        self.race = Race.objects.create(
            name="Test Race",
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