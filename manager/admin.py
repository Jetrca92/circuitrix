from django.contrib import admin

from manager.models import User, Manager, Country, Team

# Register your models here.
admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Country)
admin.site.register(Team)