from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, AddressViewSet


router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')


urlpatterns = [
path('profile/', ProfileViewSet.as_view({'get':'retrieve','patch':'partial_update'})),
path('', include(router.urls)),
]