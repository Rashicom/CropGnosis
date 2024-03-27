from django.urls import path, include
from .views import admin_views, customer_views

urlpatterns = [
    
    path("subscription-check-out", customer_views.SubscriptionCheckOut.as_view()),
    path("payment-success-callback", customer_views.PaymentSuccessCallback.as_view()),
    path("payment-cancell-callback", customer_views.PaymentSuccessCallback.as_view()),
    
]