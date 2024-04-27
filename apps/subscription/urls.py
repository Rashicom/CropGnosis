from django.urls import path, include
from .views import admin_views, customer_views, mentor_views

urlpatterns = [
    
    path("subscription-checkout", customer_views.SubscriptionCheckOut.as_view()),
    path("addon-checkout", customer_views.AddonPlanCheckout.as_view()),
    path("mentorsubscription-checkout", customer_views.MentorSubscriptionCheckout.as_view()),
    path("payment-success-callback", customer_views.PaymentSuccessCallback.as_view()),
    path("payment-cancell-callback", customer_views.PaymentCancellCallback.as_view()),
    

    path('mentor/add-basementorplan', mentor_views.AddMentorSubscriptionPlan.as_view()),
    path('mentor/update-basementorplan/<str:pk>', mentor_views.UpdateMentorSubscriptionPlan.as_view()),
    path('mentor/delete-basementorplan/<str:pk>', mentor_views.DeleteMentorSubscriptionPlan.as_view()),
]