from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# User Registration
class UserRegistration(APIView):

    def post(self, request, *args, **kwargs):
        pass



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
