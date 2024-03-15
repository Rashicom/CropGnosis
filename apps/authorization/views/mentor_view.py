from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from ..serializer.mentor_serializer import MentorRegistrationSerializer, MentorAddressSerializer, MentorAccountSerializer
from ...common.utils.exceptions import BadRequestException, PermissionDeniedException
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Accounts, Address

# Mentor registration
# Mentor account defaultly not activated
class MentorRegistration(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = MentorRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # user registration send email in signals

        # serizer modified created method doesn't update add my_address field
        # so we are eplicitly adding my_addresses field to the response
        data = serializer.data
        data["my_addresses"] = serializer.validated_data.get("my_addresses")

        self.success_message = "User registered successfully"
        return Response(data)
    

# login for mentor users
class UserLogin(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise BadRequestException
        
        user = authenticate(request,email=email, password=password)
        
        # user must be activated
        if not user.is_activated:
            self.error_message = "uer is in inactive status"
            raise PermissionDeniedException
        
        elif user is not None and user.user_type=="MENTOR":
            refresh = RefreshToken.for_user(user)
            self.success_message = "Login successful"
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            })
        
        else:
            self.error_message = "User not found"
            return Response(status=401)
        

# update Account
class UpdateMentorAccount(generics.GenericAPIView):
    serializer_class = MentorAccountSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        account = request.user
        serializer = self.serializer_class(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.success_message = "Account updated successfully"
        return Response(serializer.data)



# update addrss
class MentorAccountAddress(generics.GenericAPIView):
    serializer_class = MentorAddressSerializer
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):
        serializer = self.serializer_classr(request.user)
        return Response(serializer.user)
    

    def path(self, request, *args, **kwargs):
        account = request.user
        address = account.my_addresses.all().last()
        serializer = self.serializer_class(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.success_message = "Address updated successfully"
        return Response(serializer.data, status=200)