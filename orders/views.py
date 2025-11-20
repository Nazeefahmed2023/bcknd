from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .kafka_producer import get_producer


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()

        # Fix: use order.status (NOT Order.status)
        if order.status in ['DELIVERED', 'CANCELLED']:
            return Response({'detail': 'Cannot cancel'}, status=400)

        order.status = 'CANCELLED'
        order.save()

        # produce kafka event
        p = get_producer()
        p.send('order.updated', {
            'order_id': order.id,
            'status': order.status
        })
        p.flush()

        return Response({'detail': 'cancelled'})
