from django.test import TestCase
from manager.models import Championship, Team, Manager, User
from races.helpers import assign_championship  # Import your assign_championship function

class AssignChampionshipTestCase(TestCase):
    
    def test_assign_teams(self):
        # Create 35 Users, Managers, and Teams for testing
        for i in range(35):
            # Append a unique identifier to the username
            user = User.objects.create(username=f"user{i + 1}_test", password="password", email=f"user{i + 1}@gmail.com")
            manager = Manager.objects.create(name=f"Manager {i + 1}", user=user)
            team = Team.objects.create(name=f"Team {i + 1}", owner=manager)

        # Call the assign_championship function for each team
        for team in Team.objects.all():
            assign_championship(team)

        # Verify the results
        # You can use assertions to check that the teams have been assigned to the correct championships.
        # For example, you can check that the number of teams in each championship is within the schema limits.

        # Example assertions:
        division1_championships = Championship.objects.filter(division=1)
        for championship in division1_championships:
            self.assertTrue(championship.teams.count() <= 10)

        division2_championships = Championship.objects.filter(division=2)
        for championship in division2_championships:
            self.assertTrue(championship.teams.count() <= 10)

        division3_championships = Championship.objects.filter(division=3)
        for championship in division3_championships:
            self.assertTrue(championship.teams.count() <= 10)

        # Add more assertions as needed to validate the results.