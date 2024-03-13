from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from ..serializer.customer_serializer import UserRegistrationSerializer
import random


# User Registration
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

        if not email or password:
            pass
            
        return Response(status=200)
    

class VarifyOtp(APIView):
    
    def post(self, request):
        pass


class AddressView(generics.GenericAPIView):

    def post(self, request):
        pass
