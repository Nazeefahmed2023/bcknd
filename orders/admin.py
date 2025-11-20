from django.contrib import admin
from .models import Order, OrderItem, DeliveryAssignment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    search_fields = ("id", "user__username", "razorpay_order_id")


@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = ("order", "delivery_boy", "assigned_at", "current_lat", "current_lng")
    search_fields = ("order__id", "delivery_boy__username")
