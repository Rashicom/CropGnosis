from rest_framework import serializers
from ..models import Accounts, Address


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        
        fields = ["name","contact_number","email", "password", "user_type"]
        extra_kwargs = {
            "name":{"required":True},
            "contact_number":{"required":True},
            "email":{"required":True},
            "password":{"write_only":True}
        }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["account","place","city","state","zip_code","about"]
        extra_kwargs = {
            "place":{"required":True},
            "city":{"required":True},
            "state":{"required":True},
            "zip_code":{"required":True}
        }
