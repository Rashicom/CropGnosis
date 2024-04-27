from typing import Iterable
from django.db import models
import uuid
from apps.common.utils.util_methods import generate_random_alphanumeric_string
from datetime import datetime

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ["-created_at"]


"""-----------------Farmer  Subsctiptions-----------------"""
# subscription plans
class BaseSubscriptionPlans(BaseModel):
    name = models.CharField(max_length=100)
    discription = models.CharField(max_length=150)
    features = models.ManyToManyField(
        to="subscription.EssentialFeatures",
        related_name="base_plan_features"
    )
    total_price = models.FloatField() # cumulative price of all features
    discounted_price = models.FloatField() # base subscription price
    crop_field_count = models.IntegerField()
    # for now only monthly plans are available
    plan_validity = models.IntegerField(default=30) # in days



# plan features
class EssentialFeatures(BaseModel):
    """
    This feature is a kind of permission, feature char name is used as the permission name
    any user access the perticular feature we are checking the feature name for the permission checking
    main features:
        satellite_data, satellite_images, vegitation idex, vegitation
    """
    PERIODIC_CHOICES = {
        "DAILY": "DAILY",
        "MONTHLY":"MONTHLY",
        "YEARLY":"YEARLY",
    }
    # for now only monthly plans are avalable
    periodicity = models.CharField(max_length=10, choices=PERIODIC_CHOICES, default="MONTHLY", null=True, blank=True)
    feature = models.CharField(max_length=100)
    remark = models.TextField()
    feature_price = models.FloatField() # per day



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
        through="subscription.PlanFeaturesThrough" ,
    )
    valied_till = models.DateField()

    @property
    def is_expired(self):
        # return bool of expired status
        return self.valied_till < datetime.now().date()


    class meta:
        ordering = ["-created_at"]



# through table for plan lass method, but afeatures m2m connection to plan peature tabele
# through table contain the feature is the part of base plan of addon
class PlanFeaturesThrough(BaseModel):

    TYPE_CHOICES = {
        "BASE_SUBSCRIPTION_FEATURE":"BASE_SUBSCRIPTION_FEATURE",
        "ADD_ON_FEATURE":"ADD_ON_FEATURE",
    }

    base_subscription = models.ForeignKey(
        to="subscription.AccountSubscription",
        on_delete=models.CASCADE,
    )
    subscription_features = models.ForeignKey(
        to="subscription.EssentialFeatures",
        on_delete=models.CASCADE,
    )
    feature_type = models.CharField(choices=TYPE_CHOICES, default="BASE_SUBSCRIPTION_FEATURE")



"""-----------------Mentor  Subsctiptions-----------------"""
# Mentor base subscription
class MentorBaseSubscriptionPlans(BaseModel):
    """
    Mentors can have 3 periodicity plans.
    they can add up to 3 plans. all the plans list outed for farmers
    """
    PERIODICITY_CHOICES = {
        "WEEKLY": "WEEKLY",
        "MONTHLY": "MONTHLY",
        "YEARLY": "YEARLY",
    }
    mentor = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_plans"
    )
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES)
    amount = models.FloatField()



# Mentor subscription
# Mentor subscription not depends on the base plan
# user can contact mentor even theire base plan is expired if they have a mentor plan
# Data processing and data collection are suspended if base plan is expired, but they can see the previously generated data
class MentorSubscriptions(BaseModel):
    mentor_base_plan = models.ForeignKey(
        to="subscription.MentorBaseSubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="mentor_subscription_set"
    )
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




# TODO: iot subscription table
# class BaseIoTSubscriptionPlans(BaseModel):

# TODO: data analatics service subscription plans
# class BaseDataAnalaticsSubscriptionPlans(BaseModel):



"""--------------------  Payments   --------------------"""
# payment
class PaymentTransactions(BaseModel):
    PAID_FOR_CHOICES = {
        "BASE_SUBSCRIPTION_PLAN":"BASE_SUBSCRIPTION_PLAN",
        "ADD_ON_PLAN":"ADD_ON_PLAN",
        "MENTOR":"MENTOR",
        "IOT_INTEGRATION":"IOT_INTEGRATION"
    }
    paid_for = models.CharField(choices=PAID_FOR_CHOICES, max_length=50)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=150, null=True, blank=True)

    # payed for foreign keys
    subscription_plan = models.ForeignKey(
        to="subscription.BaseSubscriptionPlans", 
        on_delete=models.CASCADE,
        related_name="purchased_set",
        blank=True, null=True
    )

    addon = models.ForeignKey(
        to="subscription.EssentialFeatures",
        on_delete=models.CASCADE,
        related_name="forme_transactions",
        blank=True, null=True
    )

    mentor_plan = models.ForeignKey(
        to="subscription.MentorBaseSubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="forme_transactions",
        blank=True, null=True
    )

    amount = models.FloatField(null=True, blank=True)
    invoice_pdf = models.FileField(upload_to="invoices", null=True, blank=True)
    created_by = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_transactions"
    )

    payment_response = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = generate_random_alphanumeric_string(length=16)
        super(PaymentTransactions,self).save(*args, **kwargs)
