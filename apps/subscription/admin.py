from django.contrib import admin
from .models import BaseSubscriptionPlans, EssentialFeatures, PaymentTransactions, AccountSubscription, MentorBaseSubscriptionPlans, MentorSubscriptions, PlanFeaturesThrough


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

class RouteThroughInline(admin.TabularInline):
    model = PlanFeaturesThrough
    extra = 1


@admin.register(AccountSubscription)
class AccountSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "base_plan",
        "get_feature_display",
        "valied_till"
    )
    inlines = [RouteThroughInline]

    def get_feature_display(self, obj):
        if obj.plan_features.exists():
            return ", ".join([feature.feature if feature.feature else "Unknown" for feature in obj.plan_features.all()])
        return ""
    
    get_feature_display.short_description = "Plan Features"
    get_feature_display.admin_order_field = "feature__feature"

@admin.register(MentorSubscriptions)
class MentorSubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        "farmer",
        "mentor",
        "valied_till"
    )

@admin.register(MentorBaseSubscriptionPlans)
class MentorBaseSubscriptionPlansAdmin(admin.ModelAdmin):
    list_display = (
        "mentor",
        "periodicity",
        "amount"
    )

@admin.register(PlanFeaturesThrough)
class PlanFeaturesThroughAdmin(admin.ModelAdmin):
    list_display = (
        "base_subscription",
        "subscription_features",
        "feature_type"
    )