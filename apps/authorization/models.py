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
    email = models.EmailField(max_length=150, unique=True)
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
    account = models.ForeignKey(to="authorization.Accounts", on_delete=models.CASCADE, related_name="my_addresses")

    # basic address information
    place = models.CharField(max_length=100, blank=True, null = True)
    city = models.CharField(max_length=100, blank=True, null = True)
    state = models.CharField(max_length=100, blank=True, null = True)
    zip_code = models.CharField(max_length=100, blank=True, null = True)

    about = models.TextField(blank=True, null = True)
    designation = models.CharField(max_length=50, blank=True, null = True)
    mentor_fee = models.IntegerField(blank=True, null = True)
    


# otp
class Otp(BaseModel):
    account = models.ForeignKey("authorization.Accounts", on_delete=models.CASCADE, related_name="otp_set")

    otp_code = models.CharField(max_length=50)
    is_used = models.BooleanField(default=False)



# Account subscriptions
class AccountSubscription(BaseModel):
    user = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_subscriptions"
    )
    base_plan = models.ForeignKey(
        to="subscription.BaseSubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="base_subscription_set"
    )
    plan_features = models.ManyToManyField(
        to="subscription.EssentialFeatures",
        through="authorization.PlanFeaturesThrough" ,
    )
    valied_till = models.DateField()


# through table for plan features m2m connection to plan peature tabele
# through table contain the feature is the part of base plan of addon
class PlanFeaturesThrough(BaseModel):

    TYPE_CHOICES = {
        "BASE_SUBSCRIPTION_FEATURE":"BASE_SUBSCRIPTION_FEATURE",
        "ADD_ON_FEATURE":"ADD_ON_FEATURE",
    }

    base_subscription = models.ForeignKey(
        to="authorization.AccountSubscription",
        on_delete=models.CASCADE,
    )
    subscription_features = models.ForeignKey(
        to="subscription.EssentialFeatures",
        on_delete=models.CASCADE,
    )
    feature_type = models.CharField(choices=TYPE_CHOICES)




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
    mentor = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_farmers"
    )
    valied_till = models.DateField()



"""------------------WALLET-----------------------------"""
# TODO:wallet model
