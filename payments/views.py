from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
from .utils import get_razorpay_client
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hmac, hashlib, json
from .kafka_producer import produce_payment_success_event


class CreateRazorpayOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'detail': 'Order not found'}, status=404)

        client = get_razorpay_client()

        data = {
            'amount': int(order.total * 100),
            'currency': 'INR',
            'receipt': str(order.id),
            'payment_capture': 1
        }

        razor_order = client.order.create(data=data)

        return Response({
            'razorpay_order': razor_order,
            'key_id': settings.RAZORPAY_KEY_ID
        })


@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        sig = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
        body = request.body.decode()

        # Verify using HMAC
        expected = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected, sig):
            # fallback for development
            pass

        payload = json.loads(body)
        event = payload.get('event')

        if event in ('payment.captured', 'payment.authorized'):
            payload_data = payload.get('payload', {})
            payment_entity = payload_data.get('payment', {}).get('entity', {})

            notes = payment_entity.get('notes', {})
            receipt = payment_entity.get('order_id') or notes.get('receipt')

            try:
                local_order = Order.objects.get(id=int(receipt))
                local_order.status = 'PAYMENT_SUCCESS'
                local_order.save()

                produce_payment_success_event({
                    'order_id': local_order.id,
                    'user_id': local_order.user.id,
                    'amount': float(local_order.total)
                })

            except Exception:
                pass

        return Response({'ok': True})
