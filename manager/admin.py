from django.contrib import admin

from manager.models import (
    User, Manager, Team, Country, RaceMechanic, LeadDesigner, Driver, Car, 
    Championship, Racetrack, Race, RaceResult, RaceOrders, TeamPoints, DriverPoints
)


admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(RaceMechanic)
admin.site.register(LeadDesigner)
admin.site.register(Country)
admin.site.register(Car)
admin.site.register(Championship)
admin.site.register(Racetrack)
admin.site.register(Race)
admin.site.register(RaceResult)
admin.site.register(RaceOrders)
admin.site.register(TeamPoints)
admin.site.register(DriverPoints)
