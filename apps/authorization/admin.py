from django.contrib import admin
from .models import Accounts, Address, Otp, AccountSubscription, MentorSubscriptions


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
        "mentor_fee"
    )


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "otp_code",
        "is_used"
    )


@admin.register(AccountSubscription)
class AccountSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "base_plan",
        "valied_till"
    )


@admin.register(MentorSubscriptions)
class MentorSubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        "farmer",
        "mentor",
        "valied_till"
    )

