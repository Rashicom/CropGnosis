from django.conf import settings
import stripe
from datetime import datetime
from datetime import timedelta
from apps.common.utils.exceptions import NotFoundException, UnhandledException
from apps.subscription.models import PaymentTransactions, AccountSubscription, PlanFeaturesThrough, MentorSubscriptions

# set stripe globally
stripe.api_key = settings.STRIPE_API_KEY


class BasePayment:
    """
    This is a base class for all payments
    all payment class will be a subclass of this base class
    """
    def __init__(self):
        pass


# stripe payment
class StripePayment(BasePayment):
    def __init__(self, user_obj, transaction_obj):
        self.user = user_obj
        self.transaction = transaction_obj
        self.user_address = None
        self.stripe_customer = None

    def checkout(self):
        """
        """
        self.user_address = self.user.my_addresses
        if not self.user_address:
            raise Exception("User Must be have a valied address")

        # Check if the user has already custemer in stripe
        try:
            self.stripe_customer = stripe.Customer.retrieve(self.user_address.stripe_cus_id) if self.user_address.stripe_cus_id else None
        except Exception as e:
            # if not found it rise an exception
            self.stripe_customer = None

        # if not a stripe customer id, first create a stripe user
        if not self.stripe_customer:
            self.stripe_customer = stripe.Customer.create(
                name=self.user.name,
                email=self.user.email,
                phone=self.user.contact_number,
                shipping={
                    "address":{
                        "city": self.user_address.city,
                        "country": "India",
                        "line1": self.user_address.place,
                        "postal_code":self.user_address.zip_code,
                        "state":self.user_address.state,
                    },
                    "name":self.user.name,
                    "phone":self.user.contact_number
                }
            )
            self.user_address.stripe_cus_id = self.stripe_customer.id
            self.user_address.save()
        
        # create payment session
        checkoute_session = stripe.checkout.Session.create(
            customer=self.stripe_customer,
            line_items=[
                {
                    "price_data":{
                        "currency":"INR", # TODO: dynamically set currency
                        "unit_amount_decimal":self.transaction.amount * 100,
                        "product_data":{
                            "name":self.transaction.paid_for
                        }
                    },
                    "quantity":1
                }
            ],
            metadata={
                "transaction_id":self.transaction.transaction_id,
                # TODO: add other fields if any
            },
            billing_address_collection="auto", # TODO: change status accordingly by currency and transaction country
            mode="payment",
            success_url=settings.BASE_URL+"api/subscription/payment-success-callback?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.BASE_URL+"api/subscription/payment-cancell-callback?session_id={CHECKOUT_SESSION_ID}",
        )

        return checkoute_session
    
    def confirm_payment(self, session_id=None):
        if session_id is None:
            raise Exception("session_id is required")
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except Exception as e:
            raise Exception("Could not retrieve")
        if not session:
            raise Exception("session not found")
        
        # retrieve payment object
        payment_obj = PaymentTransactions.objects.filter(stripe_session_id=session_id).last()

        # call appropreate method for update service for accounts according to the payment for type
        if payment_obj.paid_for == "BASE_SUBSCRIPTION_PLAN":
            self._update_base_subscription_plan(payment_obj)
        elif payment_obj.paid_for == "ADD_ON_PLAN":
            self._update_add_on_plan(payment_obj)
        elif payment_obj.paid_for == "MENTOR":
            self._update_mentor(payment_obj)
        elif payment_obj.paid_for == "IOT_INTEGRATION":
            self._update_iot_integration(payment_obj)
        else:
            raise Exception("Payment type not found")

        # update payment status
        payment_obj.status = True
        payment_obj.save()
    
    
    """ --------  methods for updating services ----------"""

    def _update_base_subscription_plan(self, payment_obj):
        """
        Update user subscription table
        """

        # validity is the todays date + number of days of validity
        validity_till = datetime.now().date() + timedelta(days=payment_obj.subscription_plan.plan_validity)
        subscription_obj = AccountSubscription.objects.create(
            user=self.user,
            base_plan=payment_obj.subscription_plan,
            valied_till=validity_till
        )
        subscription_obj.plan_features.set(payment_obj.subscription_plan.features.all())


    def _update_add_on_plan(self, payment_obj):
        """
        Update user subscription table
        """
        existing_plans = self.user.my_subscriptions
        if not existing_plans:
            raise Exception("User must have a subscription")

        # fetch recently created subscription plan and add addon to it
        latest_subscription = AccountSubscription.objects.latest("created_at")
        
        # update through , through table
        PlanFeaturesThrough.objects.create(
            base_subscription=latest_subscription,
            subscription_features=payment_obj.addon,
            feature_type="ADD_ON_FEATURE"
        )


    def _update_mentor(self, payment_obj):
        """
        Update user subscription table
        """
        # Update mentor subscription plan
        if payment_obj.mentor_plan.periodicity == "WEEKLY":
            valied_till=datetime.now().date() + timedelta(days=7)
        elif payment_obj.mentor_plan.periodicity == "MONTHLY":
            valied_till=datetime.now().date() + timedelta(days=30)
        elif payment_obj.mentor_plan.periodicity == "YEARLY":
            valied_till=datetime.now().date() + timedelta(days=365)


        MentorSubscriptions.objects.create(
            mentor_base_plan=payment_obj.mentor_plan,
            farmer=payment_obj.created_by,
            mentor=payment_obj.mentor,
            valied_till=valied_till
        )

    def _update_iot_integration(self, payment_obj):
        """
        Update user subscription table
        """
        pass

        
                
                
            