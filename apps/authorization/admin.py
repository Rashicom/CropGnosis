from django.contrib import admin
from .models import Accounts, Address, Otp


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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "place",
        "city",
        "state",
        "zip_code",
        "about",
        "designation",
    )


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "otp_code",
        "is_used"
    )

