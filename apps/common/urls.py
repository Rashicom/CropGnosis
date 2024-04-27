from django.urls import path, include
from . import views

urlpatterns = [
    path('features', views.ListFeatures.as_view()),
    path('base-plans', views.ListBasePlan.as_view()),
    path("mentor-plans", views.ListBaseMentorSubscriptionPlans.as_view())
]