from rest_framework import serializers
from ..models import Accounts, Address
from django.db import transaction
from django.contrib.auth.hashers import make_password


# mentor address serializer
class MentorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["place","city","state","zip_code","about", "designation", "mentor_fee"]
        extra_kwargs = {
            "place":{"required":True},
            "city":{"required":True},
            "state":{"required":True},
            "zip_code":{"required":True},
            "designation":{"required":True},
            "mentor_fee":{"required":True},
        }

class MentorRegistrationSerializer(serializers.ModelSerializer):
    my_addresses = MentorAddressSerializer()
    class Meta:
        model = Accounts
        
        fields = ["name","contact_number","email", "password", "user_type", "my_addresses"]
        extra_kwargs = {
            "name":{"required":True},
            "contact_number":{"required":True},
            "email":{"required":True},
            "password":{"write_only":True}
        }
    
    def create(self, validated_data):
        address = validated_data.pop("my_addresses")
        password = validated_data.pop("password")
        with transaction.atomic():
            account = Accounts.objects.create(
                **validated_data, user_type="MENTOR",
                is_activated=False,
                password = make_password(password)
            )
            Address.objects.create(**address, account=account)
        return account