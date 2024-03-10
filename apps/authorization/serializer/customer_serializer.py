from rest_framework import serializers
from authorization.models import Accounts

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"
    
