import random
import redis
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def get_redis():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )
