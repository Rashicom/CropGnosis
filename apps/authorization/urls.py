from django.urls import path, include
from .views import common_views, customer_views, admin_views, mentor_view

urlpatterns = [

    path('customer/registration', customer_views.UserRegistration.as_view()),
    path('customer/login', customer_views.UserLogin.as_view()),
    path('customer/address', customer_views.AccountAddress.as_view()), #get post patch


    path('mentor/registration', mentor_view.MentorRegistration.as_view()),
    path('mentor/login', mentor_view.UserLogin.as_view()),
    path('mentor/update-account', mentor_view.UpdateMentorAccount.as_view()),
    path('mentor/address', mentor_view.MentorAccountAddress.as_view()),


]
