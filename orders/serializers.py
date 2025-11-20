from rest_framework import serializers
from .models import Order, OrderItem, DeliveryAssignment
from catalog.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "total_amount",
            "status",
            "items",
            "created_at",
            "updated_at",
            "payment_id",
            "razorpay_order_id",
            "razorpay_payment_id",
            "razorpay_signature",
            "delivery_address",
        ]


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = DeliveryAssignment
        fields = ["id", "order", "delivery_boy", "assigned_at", "current_lat", "current_lng"]
