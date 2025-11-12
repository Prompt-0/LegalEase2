from django.contrib import admin
from .models import PoliceStation, LegalCase, Helpline

admin.site.register(PoliceStation)
admin.site.register(LegalCase)
admin.site.register(Helpline) # And register it
