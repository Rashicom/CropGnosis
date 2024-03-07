from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager



class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]



# User model
class Accounts(BaseModel, AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = {
    "FARMER": "FARMER",
    "MENTOR": "MENTOR",
    }

    name = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True, unique=True)
    is_activated = models.BooleanField(default=True)

    # django level permissions
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # cutorm permission roles
    is_farm_staff = models.BooleanField(default=False)

    # user type
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default="FARMER")

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



# address
class Address(BaseModel):
    account = models.ForeignKey("authorization.Accounts", on_delete=models.CASCADE, related_name="my_addresses")

    # basic address information
    place = models.CharField(max_length=100, blank=True, null = True)
    city = models.CharField(max_length=100, blank=True, null = True)
    state = models.CharField(max_length=100, blank=True, null = True)
    zip_code = models.CharField(max_length=100, blank=True, null = True)

    about = models.TextField(blank=True, null = True)
    designation = models.CharField(max_length=50, blank=True, null = True)
    


# otp
class Otp(BaseModel):
    account = models.ForeignKey("authorization.Accounts", on_delete=models.CASCADE, related_name="otp_set")

    otp_code = models.CharField(max_length=50)
    is_used = models.BooleanField(default=False)



# Account subscriptions
class AccountBaseSubscription(BaseModel):
    user = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_subscriptions"
    )
    base_plan = models.ForeignKey(
        to="subscription.SubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="base_subscription_set"
    )
    valied_till = models.DateField()



# add on plans validity on the base plan validity
# base plan can have multiple addon plans
class AddonSubscription(BaseModel):
    base_subscription = models.ForeignKey(
        to="authorization.AccountBaseSubscription",
        on_delete=models.CASCADE,
        related_name="addon_plan_set"
    )
    add_on_plan = models.ForeignKey(
        to="subscription.SubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="addon_subscription_set"
    )
    


"""-----------------Mentor  Subsctiptions-----------------"""
    
# Mentor subscription
# Mentor subscription not depends on the base plan
# user can contact mentor even theire base plan is expired if they have a mentor plan
# Data processing and data collection are suspended if base plan is expired, but they can see the previously generated data
class MentorSubscriptions(BaseModel):
    farmer = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="subscribed_mentors_set"
    )
    mentor_plan = models.ForeignKey(
        to="subscription.SubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="mentor_plan_subscription_set"
    )
    mentor = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_farmers"
        )
    valied_till = models.DateField()

