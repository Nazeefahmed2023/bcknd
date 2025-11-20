from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, Address
from .serializers import UserSerializer, AddressSerializer


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]


def retrieve(self, request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


def partial_update(self, request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)




class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer


def get_queryset(self): 
    return Address.objects.filter(user=self.request.user)


def perform_create(self, serializer):
    serializer.save(user=self.request.user)