from rest_framework import serializers
from ..subscription.models import BaseSubscriptionPlans, EssentialFeatures, MentorBaseSubscriptionPlans


# features serializer
class EssentialFeaturSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssentialFeatures
        exclude = ["created_at", "updated_at"]


# balse plan serializer
class BasePlanSerializer(serializers.ModelSerializer):
    features = EssentialFeaturSerializer(read_only=True,many=True)
    class Meta:
        model = BaseSubscriptionPlans
        exclude = ["created_at", "updated_at"]


class MentorBaseSubscriptionPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorBaseSubscriptionPlans
        exclude = ["created_at", "updated_at"]