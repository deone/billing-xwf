from django.contrib import admin
from .models import Radcheck

@admin.register(Radcheck)
class RadcheckAdmin(admin.ModelAdmin):
    pass
