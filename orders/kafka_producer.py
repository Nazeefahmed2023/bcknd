from kafka import KafkaProducer
import json
from django.conf import settings

producer = None

def get_producer():
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    return producer

def produce_payment_success_event(payload):
    p = get_producer()
    p.send('payment.success', payload)
    p.flush()
