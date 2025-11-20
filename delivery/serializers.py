from cart import serializers
from .models import DeliveryAssignment
from orders.serializers import OrderSerializer


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = DeliveryAssignment
        fields = [
            "id",
            "order",
            "delivery_boy",
            "assigned_at",
            "current_lat",
            "current_lng",
            "last_updated",
        ]