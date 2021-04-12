from django.contrib import admin

from .models import Flights, Airport, Passenger

class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
# Register your models here.

admin.site.register(Airport)
admin.site.register(Flights, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)