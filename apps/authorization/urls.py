from django.urls import path, include
from .views import common_views, customer_views, admin_views, mentor_view

urlpatterns = [

    path('customer/user-registration', customer_views.UserRegistration.as_view()),
    path('customer/login', customer_views.UserLogin.as_view()),
    path('customer/address', customer_views.AccountAddress.as_view()),

    path('mentor/registration', mentor_view.MentorRegistration.as_view())


]
