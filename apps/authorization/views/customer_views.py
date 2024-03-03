from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class UserLogin(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(status=200)