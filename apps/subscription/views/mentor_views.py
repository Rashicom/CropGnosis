from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from apps.subscription.models import MentorBaseSubscriptionPlans
from apps.subscription.serializer.mentor_serializer import MentorBaseSubscriptionPlansSerializer


# mentor plans
class AddMentorSubscriptionPlan(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MentorBaseSubscriptionPlansSerializer
    queryset = MentorBaseSubscriptionPlans.objects.all()

    def get_queryset(self):
        user = self.request.user
        return user.my_plans.all()

    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)


# update mentor plan
class UpdateMentorSubscriptionPlan(generics.UpdateAPIView):
    http_method_names = ["PATCH"]
    permission_classes = [IsAuthenticated]
    serializer_class = MentorBaseSubscriptionPlansSerializer
    queryset = MentorBaseSubscriptionPlans.objects.all()


# Detele mentor base plan
class DeleteMentorSubscriptionPlan(generics.UpdateAPIView):
    http_method_names = ["DELETE"]
    permission_classes = [IsAuthenticated]
    serializer_class = MentorBaseSubscriptionPlansSerializer
    queryset = MentorBaseSubscriptionPlans.objects.all()