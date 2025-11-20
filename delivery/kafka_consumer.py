from kafka import KafkaConsumer
import json
from orders.models import Order
from delivery.models import DeliveryAssignment
from django.contrib.auth import get_user_model

User = get_user_model()


def start_delivery_consumer():
    """
    Kafka consumer that assigns a delivery boy to an order.
    Topic: 'order_placed'
    """
    consumer = KafkaConsumer(
        "order_placed",
        bootstrap_servers=["kafka:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="delivery_group",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    print("🚚 Kafka Delivery Consumer Started... Listening for orders")

    for message in consumer:
        data = message.value
        print("📦 New order event received:", data)

        order_id = data.get("order_id")
        if not order_id:
            print("❌ No order_id in event")
            continue

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            print(f"❌ Order {order_id} does not exist")
            continue

        # For now, assign ANY user marked as a delivery boy
        delivery_boy = User.objects.filter(is_staff=True).first()

        if not delivery_boy:
            print("❌ No delivery boy available")
            continue

        # Create Delivery Assignment
        assignment, created = DeliveryAssignment.objects.get_or_create(
            order=order,
            defaults={"delivery_boy": delivery_boy},
        )

        if created:
            print(f"✅ Delivery boy {delivery_boy.username} assigned to Order #{order_id}")
        else:
            print(f"ℹ Order #{order_id} already had a delivery assignment")

        # Update order status
        order.status = "OUT_FOR_DELIVERY"
        order.save()

        print(f"🚀 Order #{order_id} status updated to OUT_FOR_DELIVERY")
