from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from django.conf import settings
import json
import time
from notifications.tasks import send_order_notification

class Command(BaseCommand):
    help = "Runs the Kafka consumer for notifications."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting notifications Kafka consumer..."))

        while True:
            try:
                consumer = KafkaConsumer(
                    'notification.send',
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='latest',
                    group_id="notification_group"
                )

                for msg in consumer:
                    payload = msg.value
                    user_id = payload.get("user_id")
                    message = payload.get("message")

                    self.stdout.write(self.style.WARNING(
                        f"Sending notification to user {user_id}: {message}"
                    ))

                    send_order_notification.delay(user_id, message)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Notification consumer error: {e}"))
                time.sleep(5)
