from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..subscription.models import BaseSubscriptionPlans, EssentialFeatures
from .serializers import BasePlanSerializer, EssentialFeaturSerializer




# List fetures
class ListFeatures(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = EssentialFeatures.objects.all()
    serializer_class = EssentialFeaturSerializer

# List all base plans
class ListBasePlan(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = BaseSubscriptionPlans.objects.all()
    serializer_class = BasePlanSerializer
