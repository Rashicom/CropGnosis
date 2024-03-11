from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..serializer.customer_serializer import UserRegistrationSerializer


# User Registration
class UserRegistration(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.success_message = "User registered successfully"
        return Response(serializer.data)


# login for farmers and staff farmers
class UserLogin(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(status=200)
    

class VarifyOtp(APIView):
    
    def post(self, request):
        pass


class AddressView(generics.GenericAPIView):

    def post(self, request):
        pass
