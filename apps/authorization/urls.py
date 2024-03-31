from django.urls import path, include
from .views import customer_views, admin_views, mentor_view

urlpatterns = [
    path('customer/registration', customer_views.UserRegistration.as_view()),
    path('customer/login', customer_views.UserLogin.as_view()),
    path('customer/address', customer_views.AccountAddress.as_view()), #get post patch


    path('mentor/registration', mentor_view.MentorRegistration.as_view()),
    path('mentor/login', mentor_view.UserLogin.as_view()),
    path('mentor/update-account', mentor_view.UpdateMentorAccount.as_view()),
    path('mentor/address', mentor_view.MentorAccountAddress.as_view()),
    path('mentor/add-basementorplan', mentor_view.AddMentorSubscriptionPlan.as_view()),
    path('mentor/update-basementorplan/<str:pk>', mentor_view.UpdateMentorSubscriptionPlan.as_view()).
    path('mentor/delete-basementorplan/<str:pk>', mentor_view.DeleteMentorSubscriptionPlan.as_view())

]
