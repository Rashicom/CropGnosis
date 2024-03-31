from rest_framework import generics
from rest_framework.response import Response
from ..models import EssentialFeatures, PaymentTransactions, BaseSubscriptionPlans
from ..serializer.admin_serializer import EssentiaFeaturelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.common.utils.exceptions import BadRequestException
from django.shortcuts import redirect, render
from ..payments import StripePayment
from apps.authorization.models import Accounts



# Subscribe to base plan
class SubscriptionCheckOut(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request):
        """
        Subscribe to a Base subscription plan
        accept : subscription_plan <uuid>
        """

        # TESTING REMOVE IN PRODUCTION
        created_by = Accounts.objects.filter(email="rashi.kp484@gmail.com").last()
        subscription_plan_uuid = "b04a3dd4-7c7a-48e7-933d-b8656b6e595d"

        # PRODUCTION CONFIG
        # subscription_plan_uuid = request.data.get("subscription_plan")
        # created_by = request.user

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
            # created_by = request.user
            created_by = created_by
        )

        try:
            payment = StripePayment(created_by, transaction)
            checkout_session = payment.checkout()
        except Exception as e:
            print(e)
            self.error_message = "Payment Failed"
            return Response(status=500)
        
        # update session id in db
        transaction.stripe_session_id = checkout_session.id
        transaction.save()

        # redirect to stripe checkout
        return redirect(checkout_session.url, status=300)
    
    def get(self, request):
        """
        this is for test, html is handled in frond end
        """
        return render(request,"checkout.html")
   


# payment success callback
class PaymentSuccessCallback(generics.GenericAPIView):

    def get(self, request):
        """
        fetch order details from stipe using settion id.
        confirm order and service and update db
        """
        # fetch oder details from stripe
        session_id = request.GET.get("session_id")
        if not session_id:
            raise BadRequestException
        
        transaction = PaymentTransactions.objects.filter(stripe_session_id=session_id, status=False).last()
        if not transaction:
            raise BadRequestException
        
        try:
            payment = StripePayment(transaction.created_by, transaction)
            payment.confirm_payment()
        except Exception as e:
            return Response(status=500)

        return Response(status=200)
    


# payment cancell callback
class PaymentCancellCallback(generics.GenericAPIView):

    def get(self, request):
        print("cancell callback : ", request.data)
        return Response(status=200)