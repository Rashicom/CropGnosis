from rest_framework import serializers
from apps.subscription.models import MentorBaseSubscriptionPlans


class MentorBaseSubscriptionPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorBaseSubscriptionPlans
        exclude = ["mentor"]