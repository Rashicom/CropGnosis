from django.conf import settings
import stripe
from apps.common.utils.exceptions import NotFoundException, UnhandledException

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
            success_url=f"{settings.BASE_URL}api/subscription/payment-success-callback",
            cancel_url=f"{settings.BASE_URL}api/subscription/payment-success-callback",
        )

        return checkoute_session
                
                
            