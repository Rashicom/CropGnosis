from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from ..serializer.mentor_serializer import MentorRegistrationSerializer

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