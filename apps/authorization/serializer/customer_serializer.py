from rest_framework import serializers
from ..models import Accounts

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        
        fields = ["name","contact_number","email", "password"]
        extra_kwargs = {
            "name":{"required":True},
            "contact_number":{"required":True},
            "email":{"required":True},
            "password":{"write_only":True}
        }