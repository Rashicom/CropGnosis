from django.db import models
import uuid

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


# subscription plans
class SubscriptionPlans(BaseModel):
    PLAN_TYPE_CHOICES = {
        "BASE_SUBSCRIPTION_PLAN":"BASE_SUBSCRIPTION_PLAN",
        "ADD_ON_PLAN":"ADD_ON_PLAN",
        "MENTOR":"MENTOR"
    }
    name = models.CharField(max_length=100)
    plan_type = models.CharField(choices=PLAN_TYPE_CHOICES)
    discription = models.CharField(max_length=150)

    # plan features
    price = models.FloatField()
    plan_validity = models.IntegerField() # in days

    

class BasePlansFeatures(models.Model):
    base_plan = models.ForeignKey(
        to="subscription.SubscriptionPlans",
        on_delete=models.CASCADE,
        related_name="base_plan_features"
    )
    crop_field_count = models.IntegerField()
    sattalite_data = models.BooleanField(default=True)
    iot_integration = models.BooleanField()
    data_analatics = models.BooleanField()



# payment
class PaymentTransactions(BaseModel):
    PAID_FOR_CHOICES = {
        "BASE_SUBSCRIPTION_PLAN":"BASE_SUBSCRIPTION_PLAN",
        "ADD_ON_PLAN":"ADD_ON_PLAN",
        "MENTOR":"MENTOR"
    }

    paid_for = models.CharField(choices=PAID_FOR_CHOICES, max_length=50)

    # payed for foreign keys
    subscription_plan = models.ForeignKey(
        to="subscription.SubscriptionPlans", 
        on_delete=models.CASCADE,
        related_name="purchased_set",
        blank=True, null=True
    )

    mentor = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="forme_transactions",
        blank=True, null=True
    )

    amount = models.FloatField(null=True, blank=True)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    invoice_pdf = models.FileField(upload_to="invoices", max_length=5000, null=True, blank=True)
    created_by = models.ForeignKey(
        to="authorization.Accounts",
        on_delete=models.CASCADE,
        related_name="my_transactions"
    )

    payment_response = models.TextField(null=True, blank=True, manull=True, blank=True)
    status = models.BooleanField(default=False)

