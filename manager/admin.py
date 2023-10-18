from django.contrib import admin

from manager.models import User, Manager, Team, Country, RaceMechanic, LeadDesigner, Driver, Car

# Register your models here.
admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(RaceMechanic)
admin.site.register(LeadDesigner)
admin.site.register(Country)
admin.site.register(Car)
