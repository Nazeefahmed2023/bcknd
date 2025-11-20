from django.contrib import admin
from .models import DeliveryAssignment


@admin.register(DeliveryAssignment)
class DeliveryAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "delivery_boy",
        "assigned_at",
        "current_lat",
        "current_lng",
        "last_updated",
    )
    search_fields = ("order__id", "delivery_boy__username")
