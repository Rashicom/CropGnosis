from rest_framework import generics
from rest_framework.response import Response
from ..models import EssentialFeatures, PaymentTransactions, BaseSubscriptionPlans
from ..serializer.admin_serializer import EssentiaFeaturelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.common.utils.exceptions import BadRequestException
from django.shortcuts import redirect, render
from ..payments import StripePayment



# Subscribe to base plan
class SubscriptionCheckOut(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request):
        """
        Subscribe to a Base subscription plan
        accept : subscription_plan <uuid>
        """
        subscription_plan_uuid = request.data.get("subscription_plan")
        if not subscription_plan_uuid:
            self.error_message = "subscription_plan is required"
            raise BadRequestException
        
        subscription_plan = BaseSubscriptionPlans.objects.filter(pk=subscription_plan_uuid).last()
        if not subscription_plan:
            self.error_message = "Subscription plan not found"
            raise BadRequestException
        
        # if base plan exists, create transaction
        transaction = PaymentTransactions.objects.create(
            paid_for = "BASE_SUBSCRIPTION_PLAN",
            subscription_plan = subscription_plan,
            amount = subscription_plan.discounted_price,
            created_by = request.user
        )

        try:
            payment = StripePayment(request.user, transaction)
            checkout_session = payment.checkout()
        except Exception as e:
            print(e)
            self.error_message = "Payment Failed"
            return Response(status=500)
        return redirect(checkout_session.url, status=300)
    
    def get(self, request):
        """
        this is for test, html is handled in frond end
        """
        return render(request,"checkout.html")
   


# payment success callback
class PaymentSuccessCallback(generics.GenericAPIView):

    def post(self, request):
        print(request.data)
        return Response(status=200)
    


# payment cancell callback
class PaymentSuccessCallback(generics.GenericAPIView):

    def post(self, request):
        print(request.data)
        return Response(status=200)