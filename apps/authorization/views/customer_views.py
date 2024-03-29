from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from ..serializer.customer_serializer import UserRegistrationSerializer, AddressSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ...common.utils.exceptions import BadRequestException, PermissionDeniedException
from ..models import Accounts, Address


# Farmer User Registration
class UserRegistration(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # user registration send email in signals

        self.success_message = "User registered successfully"
        return Response(serializer.data)


# login for farmers and staff farmers
class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise BadRequestException
        
        user = authenticate(request,email=email, password=password)

        # user must be activated
        if user and not user.is_activated:
            self.error_message = "uer is in inactive status"
            raise PermissionDeniedException
        
        elif user is not None and user.user_type=="FARMER":
            refresh = RefreshToken.for_user(user)
            self.success_message = "Login successful"
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            })
        
        else:
            self.error_message = "User not found"
            return Response(status=401)
    


class AccountAddress(generics.GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        address = Address.objects.filter(account=request.user).last()
        if not address:
            return Response({"data":"address not found"},status=200)
        serializer = self.serializer_class(address)
        
        self.succuss_message = "Address fetched successfully"
        return Response(serializer.data)
        

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data={**request.data, "account":request.user.pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.succuss_message = "Address created successfully"
        return Response(serializer.data)
    

    def patch(self, request, *args, **kwargs):
        address = Address.objects.filter(account=request.user).last()
        if not address:
            self.error_message = "Address not found"
            raise BadRequestException
        serializer = self.serializer_class(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.succuss_message = "Address updated successfully"
        return Response(serializer.data)



class UpdateAccount(generics.GenericAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args , **kwargs):
        pass

