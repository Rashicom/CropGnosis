from rest_framework import generics
from rest_framework.response import Response
from ..models import EssentialFeatures, PaymentTransactions, BaseSubscriptionPlans
from ..serializer.admin_serializer import EssentiaFeaturelSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.common.utils.exceptions import BadRequestException
from django.shortcuts import redirect, render
from ..payments import StripePayment
from apps.authorization.models import Accounts
from ..models import AccountSubscription, EssentialFeatures



"""-------------------------CHECK OUTS------------------------"""

# Base plan Subscription checkout
class SubscriptionCheckOut(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request):
        """
        Subscribe to a Base subscription plan
        accept : subscription_plan <uuid>
        """

        # TESTING REMOVE IN PRODUCTION
        created_by = Accounts.objects.filter(email="farmer1@gmail.com").last()
        subscription_plan_uuid = "93002d13-20f4-4530-9738-9966fb68939b"

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
    

# Addon plan checkout
class AddonPlanCheckout(generics.GenericAPIView):
    
    def post(self, request):
        """
        Subscribe to a Base subscription plan
        accept : addon_plan <uuid>
        """

        # TESTING REMOVE IN PRODUCTION
        user = Accounts.objects.filter(email="farmer1@gmail.com").last()
        addon_plan_uuid = "3a099c72-1ad0-4b15-baa6-c3324e74ee95"

        # PRODUCTION CONFIG
        # addon_plan_uuid = request.data.get("addon_plan")
        # created_by = request.user

        if not addon_plan_uuid:
            self.error_message = "addon plan is required"
            raise BadRequestException
        
        # if not plan found in the provided addon plan uuid
        addon_plan_obj = EssentialFeatures.objects.filter(pk = addon_plan_uuid).last()

        if not addon_plan_obj:
            self.error_message = "Addon plan not found"
            raise BadRequestException
        
        # User must be have a Valied base subscription plan to create an addon
        subscribed_plan = AccountSubscription.objects.filter(user=user).last()
        if subscribed_plan is None or subscribed_plan and subscribed_plan.is_expired:
            self.error_message = "User must have a valied subscription plan"
            return BadRequestException

        # if base plan exists, create transaction
        transaction = PaymentTransactions.objects.create(
            paid_for = "ADD_ON_PLAN",
            addon = addon_plan_obj,
            amount = addon_plan_obj.feature_price,
            # created_by = request.user
            created_by = user
        )

        try:
            payment = StripePayment(user, transaction)
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
            print("no session_id found: {session_id}")
            raise BadRequestException
        
        transaction = PaymentTransactions.objects.filter(stripe_session_id=session_id, status=False).last()
        if not transaction:
            raise BadRequestException
        
        # if payment is successful, confirm it, and activate the service
        try:
            payment = StripePayment(transaction.created_by, transaction)
            payment.confirm_payment(session_id)
        except Exception as e:
            print(e)
            return Response(status=500)

        return Response({"data":"payment succuss page"},status=200)
    


# payment cancell callback
class PaymentCancellCallback(generics.GenericAPIView):

    def get(self, request):
        # fetch oder details from stripe
        session_id = request.GET.get("session_id")
        if not session_id:
            print("no session_id found: {session_id}")
            raise BadRequestException
        
        transaction = PaymentTransactions.objects.filter(stripe_session_id=session_id, status=False).last()
        if not transaction:
            raise BadRequestException
        
        # TODO: update payment failure reason from stripe
        transaction.payment_response = "Payment failed"

        return Response({"data":"payment Failure page"},status=200)