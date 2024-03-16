from rest_framework import serializers
from ..models import EssentialFeatures

class EssentiaFeaturelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssentialFeatures
        fields = "__all__"