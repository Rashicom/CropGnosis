from rest_framework import generics
from rest_framework.response import Response
from ..models import EssentialFeatures
from ..serializer.admin_serializer import EssentiaFeaturelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import redirect


# Subscribe to base plan
class CheckOut(generics.GenericAPIView):
    def post(self, request):
        return redirect("https://www.google.com/")