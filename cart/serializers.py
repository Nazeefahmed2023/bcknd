from rest_framework import serializers
from .models import Cart, CartItem
from catalog.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
class Meta:
    model = CartItem
    fields = ['id','product','product_detail','quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
class Meta:
    model = Cart
    fields = ['id','user','updated_at','items']