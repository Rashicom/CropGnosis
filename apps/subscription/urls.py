from django.urls import path, include
from .views import admin_views, customer_views

urlpatterns = [
    
    path("check-out", customer_views.CheckOut.as_view()),
    
]