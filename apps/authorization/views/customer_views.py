from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from ..serializer.customer_serializer import UserRegistrationSerializer
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ...common.utils.exceptions import BadRequestException, UnauthorizedException
from ..models import Accounts


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

        if not email or not password:
            raise BadRequestException
        
        user = authenticate(request,email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            self.success_message = "Login successful"
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token)
            })
        else:
            self.error_message = "User not found"
            return Response(status=401)
    

