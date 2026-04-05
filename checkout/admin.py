from django.contrib import admin
from .models import Order, OrderItem, Subscription


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'order_total', 'date')
    ordering = ('-date',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'lineitem_total')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'status',
        'membership_active',
        'current_period_end',
        'stripe_customer_id',
        'stripe_subscription_id',
    )
    search_fields = ('user__username', 'user__email', 'stripe_customer_id', 'stripe_subscription_id')