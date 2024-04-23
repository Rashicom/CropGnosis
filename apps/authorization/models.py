from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from .managers import AccountManager


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]



# User model
class Accounts(BaseModel, AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = {
    "FARMER": "FARMER",
    "MENTOR": "MENTOR",
    }

    name = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=150, unique=True)
    is_activated = models.BooleanField(default=True)

    # django level permissions
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # cutorm permission roles
    is_admin = models.BooleanField(default=True, blank=True, null=True) # admin farmer
    is_farmer_staff = models.BooleanField(default=False, blank=True, null=True) # farmer can add staffs

    # user type
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default="FARMER", blank=True, null=True)
    
    def __str__(self):
        return str(self.email)
    
    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



# address
class Address(BaseModel):
    account = models.OneToOneField(to="authorization.Accounts", on_delete=models.CASCADE, related_name="my_addresses")

    # basic address information
    place = models.CharField(max_length=100, blank=True, null = True)
    city = models.CharField(max_length=100, blank=True, null = True)
    state = models.CharField(max_length=100, blank=True, null = True)
    zip_code = models.CharField(max_length=100, blank=True, null = True)

    about = models.TextField(blank=True, null = True)
    designation = models.CharField(max_length=50, blank=True, null = True)

    # stripe cus id
    stripe_cus_id = models.CharField(blank=True, null = True)



# otp
class Otp(BaseModel):
    account = models.ForeignKey("authorization.Accounts", on_delete=models.CASCADE, related_name="otp_set")

    otp_code = models.CharField(max_length=50)
    is_used = models.BooleanField(default=False)



"""------------------WALLET-----------------------------"""
# TODO:wallet model
