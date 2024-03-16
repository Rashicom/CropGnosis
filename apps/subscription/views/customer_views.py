from rest_framework import generics
from rest_framework.response import Response
from ..models import EssentialFeatures
from ..serializer.admin_serializer import EssentiaFeaturelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


