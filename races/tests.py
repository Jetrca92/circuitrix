from django.test import TestCase
from manager.models import Championship, Team, Manager, User
from races.helpers import assign_championship  # Import your assign_championship function

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