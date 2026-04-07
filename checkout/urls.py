from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('membership/', views.membership_pricing, name='membership_pricing'),
    path('subscription/create/', views.create_subscription_checkout, name='create_subscription_checkout'),
    path('subscription/success/', views.subscription_success, name='subscription_success'),
    path('premium-plans/', views.premium_plans, name='premium_plans'),
    path('wh/', views.stripe_webhook, name='stripe_webhook'),
]