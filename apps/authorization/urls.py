from django.urls import path, include
from .views import common_views, customer_views, admin_views

urlpatterns = [
    path('login/', customer_views.UserLogin.as_view()),
    
]
