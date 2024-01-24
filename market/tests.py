from django.test import TestCase
from django.utils import timezone

from market.forms import ListDriverForm, FireDriverForm, DriverBidForm
from market.helpers import list_driver, bid_driver, sell_driver
from market.models import DriverListing, Bid
from market.models import TIME_ON_MARKET_IN_DAYS
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
        self.buyer = Team.objects.create(
            owner=self.manager,
            name="Buyer Team",
            location=self.country,
            total_fans=1000,
        )

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
        # Check that no listing exists
        driver_listings = DriverListing.objects.filter(driver=self.driver, seller=self.driver.team)
        self.assertEqual(0, driver_listings.count())

        # Add form data and validate form
        form_data = {
            "confirmation": True,
            "price": 100,
        }
        form = ListDriverForm(data=form_data)
        self.assertTrue(form.is_valid())
        list_driver(self.driver.id, form.cleaned_data["price"])

        # Check if driver listing exists
        driver_listings = DriverListing.objects.filter(driver=self.driver, seller=self.driver.team)
        self.assertEqual(1, driver_listings.count())
        driver = Driver.objects.get(id=self.driver.id)
        self.assertTrue(driver.is_market_listed)

    def test_driver_listing_invalid_form(self):
        # Add form data and validate form
        form_data = {
            "confirmation": False,
            "price": 100,
        }
        form = ListDriverForm(data=form_data)
        self.assertFalse(form.is_valid())
        form2_data = {
            "confirmation": True,
            "price": "",
        }
        form2 = ListDriverForm(data=form2_data)
        self.assertFalse(form.is_valid())

    def test_driver_terminate_contract_method(self):
        # Check that no listing exists
        driver_listings = DriverListing.objects.filter(driver=self.driver, seller=self.driver.team)
        self.assertEqual(0, driver_listings.count())

        # Add form data and validate form
        form_data = {
            "confirmation": True,
        }
        form = FireDriverForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Terminate contract and check dl existance
        self.driver.terminate_contract()
        list_driver(self.driver.id, 0)
        driver_listings = DriverListing.objects.filter(price=0, seller__isnull=True)
        self.assertEqual(driver_listings.count(), 1)
        self.assertIsNone(self.driver.team)
        
        # Check if driver removed from team
        team_drivers = self.team.drivers.filter(id=self.driver.id)
        self.assertEqual(team_drivers.count(), 0)

    def test_driver_list_unlist_method(self):
        # Check if driver listed
        driver = Driver.objects.get(id=self.driver.id)
        self.assertFalse(driver.is_market_listed)
        driver.list()
        self.assertTrue(driver.is_market_listed)
        driver.unlist()
        self.assertFalse(driver.is_market_listed)

    def test_driver_fire_invalid_form(self):
        form_data = {
            "confirmation": False,
        }
        form = FireDriverForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestBidDriver(TestCase):
    
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

        self.bid_user = User.objects.create_user(username="bid_user", password="bid_password", email="bid@test.com")
        self.bid_manager = Manager.objects.create(name="Bid Manager", user=self.bid_user)
        self.bid_team = Team.objects.create(
            owner=self.bid_manager,
            name="Bid Team",
            location=self.country,
            total_fans=1000,
        )
        self.bid_team.save()

        # Create a driver and listing
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
        self.driver_listing = DriverListing.objects.create(
            driver=self.driver,
            seller=self.team,
            price=10,
        )

    def test_bid_driver(self):
        # Check that no bids exist
        bids = Bid.objects.all()
        self.assertEqual(bids.count(), 0)

        # Create form and call function
        form_data = {"amount": 11, "driver_listing": self.driver_listing}
        form = DriverBidForm(data=form_data)
        self.assertTrue(form.is_valid())
        bid_driver(self.driver.id, self.bid_team, form.cleaned_data["amount"])

        # Test that bid is created
        bid = Bid.objects.filter(bidder=self.bid_team)
        self.assertTrue(bid.count(), 1)

    def test_bid_driver_invalid_form(self):
        # Bid smaller than price
        form_data = {"amount": 9, "driver_listing": self.driver_listing}
        form = DriverBidForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Create a bid that's lower than previous bid
        form_data1 = {"amount": 120, "driver_listing": self.driver_listing}
        form1 = DriverBidForm(data=form_data1)
        self.assertTrue(form1.is_valid())
        bid_driver(self.driver.id, self.bid_team, form1.cleaned_data["amount"])
        form_data2 = {"amount": 80, "driver_listing": self.driver_listing}
        form2 = DriverBidForm(data=form_data2)
        self.assertFalse(form2.is_valid())

        # Seller makes a bid
        form_data3 = {"amount": 1000, "driver_listing": self.driver_listing}
        form3 = DriverBidForm(bidder=self.team, data=form_data3)
        self.assertFalse(form3.is_valid())


class TestDriverListingMethods(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password", email="test@example.com")
        self.seller = Manager.objects.create(name="Test Manager", user=self.user)
        self.country = Country.objects.create(name="Test Country", short_name="TC", logo_location="manager/flags/test.png")
        self.seller = Team.objects.create(
            owner=self.seller,
            name="Test Team",
            location=self.country,
            total_fans=1000,
        )
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

        self.driver_listing = DriverListing.objects.create(
                driver=self.driver,
                seller=self.seller,
                price=100,
        )
        
    def test_active_method(self):
        self.assertTrue(DriverListing.objects.filter(id=self.driver_listing.id).exists())
        self.assertTrue(self.driver_listing.active())
        self.assertTrue(self.driver_listing.is_active)

        # Deadline over
        self.driver_listing.deadline = timezone.now() - timezone.timedelta(days=1)
        self.driver_listing.save()
        self.assertFalse(self.driver_listing.active())
        self.assertFalse(self.driver_listing.is_active)

    def test_close_method(self):
        self.assertTrue(DriverListing.objects.filter(id=self.driver_listing.id).exists())
        self.assertTrue(self.driver_listing.active())
        self.assertTrue(self.driver_listing.is_active)

        # Didn't close after deadline not over
        self.driver_listing.deadline = timezone.now() + timezone.timedelta(days=1)
        self.driver_listing.save()
        self.driver_listing.close()
        self.assertTrue(self.driver_listing.is_active)

        # Close after deadline over
        self.driver_listing.deadline = timezone.now() - timezone.timedelta(days=1)
        self.driver_listing.save()
        self.driver_listing.close()
        self.assertFalse(self.driver_listing.is_active)

    def test_save_method_sets_deadline(self):

        # Deadline is set and correctly calculated
        self.assertIsNotNone(self.driver_listing.deadline)
        expected_deadline = timezone.now() + timezone.timedelta(days=TIME_ON_MARKET_IN_DAYS)
        self.assertAlmostEqual(self.driver_listing.deadline, expected_deadline, delta=timezone.timedelta(seconds=1))


class TestSellDriver(TestCase):

    def setUp(self):
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

        self.bid_user = User.objects.create_user(username="bid_user", password="bid_password", email="bid@test.com")
        self.bid_manager = Manager.objects.create(name="Bid Manager", user=self.bid_user)
        self.buyer = Team.objects.create(
            owner=self.bid_manager,
            name="Bid Team",
            location=self.country,
            total_fans=1000,
        )
        self.buyer.save()
        self.buyer1 = Team.objects.create(
            owner=self.bid_manager,
            name="Bid Team1",
            location=self.country,
            total_fans=1000,
        )
        self.buyer.save()

        self.driver = Driver.objects.create(
            team=self.team,
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

    def test_driver_sell_method(self):
        # Check if everything set up
        list_driver(self.driver.id, 5)
        driver = Driver.objects.get(id=self.driver.id)
        self.assertTrue(driver.is_market_listed)
        self.assertEqual(driver.team, self.team)
        self.assertEqual(self.buyer.drivers.filter(id=self.driver.id).count(), 0)
        driver.sell(self.buyer)
        # Check function
        
        self.assertFalse(driver.is_market_listed)
        self.assertEqual(driver.team, self.buyer)
        self.assertEqual(self.buyer.drivers.filter(id=self.driver.id).count(), 1)

    def test_sell_driver_helper(self):
        # Set driver listing and 2 bids and call function
        driver = Driver.objects.get(id=self.driver.id)
        list_driver(self.driver.id, 10)
        driver_listing = DriverListing.objects.get(driver=driver)
        bid1 = Bid.objects.create(
            driver_listing=driver_listing,
            bidder=self.buyer,
            amount=2000,
        )
        bid2 = Bid.objects.create(
            driver_listing=driver_listing,
            bidder=self.buyer1,
            amount=1500,
        )
        driver_listing.deadline = timezone.now() - timezone.timedelta(days=1)
        driver_listing.save()
        sell_driver(driver.id, driver_listing)

        # Reload driver
        driver = Driver.objects.get(id=self.driver.id)
        # Highest bidder owns driver
        self.assertEqual(self.buyer.drivers.filter(id=driver.id).count(), 1)
        self.assertEqual(self.buyer, driver.team)
        self.assertFalse(driver_listing.is_active)
        self.assertFalse(driver.is_market_listed)
        
    def sell_driver_helper_no_bids(self):
        # Set driver listing and call function
        driver = Driver.objects.get(id=self.driver.id)
        list_driver(self.driver.id, 10)
        driver_listing = DriverListing.objects.get(driver=driver)
        driver_listing.deadline = timezone.now() - timezone.timedelta(days=1)
        driver_listing.save()
        sell_driver(driver.id, driver_listing)

        # Reload driver, no changes to team
        driver = Driver.objects.get(id=self.driver.id)
        self.assertFalse(driver_listing.is_active)
        self.assertFalse(driver.is_market_listed)
        self.assertEqual(driver.team, self.team)
