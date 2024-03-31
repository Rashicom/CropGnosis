from django.contrib import admin
from .models import BaseSubscriptionPlans, EssentialFeatures, PaymentTransactions


@admin.register(BaseSubscriptionPlans)
class BaseSubscriptionPlansAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "discription",
        "total_price",
        "discounted_price",
        "crop_field_count",
        "plan_validity"
    )


@admin.register(EssentialFeatures)
class EssentialFeaturesAdmin(admin.ModelAdmin):
    list_display = (
        "feature",
        "remark",
        "feature_price"
    )


@admin.register(PaymentTransactions)
class PaymentTransactionsAdmin(admin.ModelAdmin):
    list_display = (
        "paid_for",
        "subscription_plan",
        "addon",
        "mentor_plan",
        "amount",
        "transaction_id",
        "invoice_pdf",
        "created_by",
        "payment_response",
        "status"
    )