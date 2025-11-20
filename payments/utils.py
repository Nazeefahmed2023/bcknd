import razorpay
from django.conf import settings


def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def verify_signature(payload_body, signature):
    """For webhook verification: Razorpay sends header 'X-Razorpay-Signature'"""
    client = get_razorpay_client()

    try:
        client.utility.verify_payment_signature(
            {'payload': payload_body},
            signature
        )
        return True
    except Exception:
        return False
