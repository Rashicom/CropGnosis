from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..subscription.models import BaseSubscriptionPlans, EssentialFeatures, MentorBaseSubscriptionPlans
from .serializers import BasePlanSerializer, EssentialFeaturSerializer, MentorBaseSubscriptionPlansSerializer




# List fetures
class ListFeatures(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = EssentialFeatures.objects.all()
    serializer_class = EssentialFeaturSerializer

# List all base plans
class ListBasePlan(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BaseSubscriptionPlans.objects.all()
    serializer_class = BasePlanSerializer


# List add mentor plans
class ListBaseMentorSubscriptionPlans(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MentorBaseSubscriptionPlans.objects.all()
    serializer_class = MentorBaseSubscriptionPlansSerializer

