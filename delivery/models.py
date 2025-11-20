from django.db import models
from django.conf import settings

from delivery.consumers import User
from orders.models import Order


class DeliveryBoy(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    current_order = models.ForeignKey('orders.Order', null=True, blank=True, on_delete=models.SET_NULL)


class DeliveryLocation(models.Model):
    deliveryboy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


    
class DeliveryAssignment(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="delivery"
    )
    delivery_boy = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    # For live tracking
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"