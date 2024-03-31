from typing import Iterable
from django.db import models
import uuid
from apps.common.utils.util_methods import generate_random_alphanumeric_string

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]



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
    plan_validity = models.IntegerField() # in days



# plan features
class EssentialFeatures(BaseModel):
    """
    This feature is a kind of permission, feature char name is used as the permission name
    any user access the perticular feature we are checking the feature name for the permission checking
    main features:
        satellite_data, satellite_images, vegitation idex, vegitation
    """
    feature = models.CharField(max_length=100)
    remark = models.TextField()
    feature_price = models.FloatField() # per day



# TODO: iot subscription table
# class BaseIoTSubscriptionPlans(BaseModel):

# TODO: data analatics service subscription plans
# class BaseDataAnalaticsSubscriptionPlans(BaseModel):


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
    stripe_session_id = models.CharField(max_length=50, null=True, blank=True)

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
        to="authorization.MentorBaseSubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="forme_transactions",
        blank=True, null=True
    )

    amount = models.FloatField(null=True, blank=True)
    invoice_pdf = models.FileField(upload_to="invoices", max_length=5000, null=True, blank=True)
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
