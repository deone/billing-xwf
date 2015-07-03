from django.contrib import admin
from .models import Radcheck

from .forms import RadcheckAdminForm

@admin.register(Radcheck)
class RadcheckAdmin(admin.ModelAdmin):
    pass
