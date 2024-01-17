from django.test import TestCase
from django.utils import timezone

from market.forms import SellDriverForm
from market.helpers import list_driver
from market.models import DriverListing
from manager.models import User, Manager, Country, Team, Driver


class TestListDriver(TestCase):

    def setUp(self):
        # Create a country, manager, user, team
        self.country = Country.objects.create(name="Test Country", short_name="TC", logo_location="manager/flags/test.png")
        self.user = User.objects.create_user(username="test_user", password="test_password", email="test@example.com")
        self.manager = Manager.objects.create(name="Test Manager", user=self.user)
        self.team = Team.objects.create(
            owner=self.manager,
            name="Test Team",
            location=self.country,
            total_fans=1000,
        )
        self.team.save()

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

    def test_driver_listing(self):
        form_data = {
            "confirmation": True,
            "price": 100,
        }
        form = SellDriverForm(data=form_data)
        self.assertTrue(form.is_valid())
        list_driver(self.driver.id, 100)

        # Check if driver listing exists
        driver_listings = DriverListing.objects.filter(driver=self.driver, seller=self.driver.team)
        self.assertEqual(1, driver_listings.count())

    def test_driver_listing_invalid_form(self):
        form_data = {
            "confirmation": False,
            "price": 100,
        }
        form = SellDriverForm(data=form_data)
        self.assertFalse(form.is_valid())

