from django.core.management.base import BaseCommand
from kafka import KafkaConsumer, KafkaProducer
from django.conf import settings
import json
import time
from delivery.models import DeliveryBoy
from orders.models import Order

class Command(BaseCommand):
    help = "Runs the Kafka consumer for delivery assignment."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting delivery assignment Kafka consumer..."))

        while True:
            try:
                consumer = KafkaConsumer(
                    'delivery.assign_request',
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='latest',
                    group_id="delivery_assign_group"
                )

                producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )

                for msg in consumer:
                    payload = msg.value
                    order_id = payload.get('order_id')

                    self.stdout.write(self.style.WARNING(f"Assigning delivery boy for order {order_id}..."))

                    db = DeliveryBoy.objects.filter(is_active=True).first()

                    if not db:
                        self.stdout.write(self.style.ERROR("No active delivery boys available"))
                        continue

                    Order.objects.filter(id=order_id).update(
                        status="OUT_FOR_DELIVERY"
                    )

                    out_payload = {
                        "order_id": order_id,
                        "delivery_boy_id": db.id
                    }

                    producer.send("delivery.assigned", out_payload)
                    producer.flush()

                    self.stdout.write(self.style.SUCCESS(
                        f"Assigned delivery boy {db.id} to order {order_id}"
                    ))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Consumer error: {e}"))
                time.sleep(5)
