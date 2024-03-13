from django.contrib import admin
from .models import Accounts


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "contact_number",
        "is_activated",
        "is_admin",
        "is_farmer_staff",

        "is_superuser",
        "is_staff",
        "is_active",
    )
