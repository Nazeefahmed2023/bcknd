from rest_framework import serializers
from .models import User, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id','username','first_name','last_name','email','phone']
        read_only_fields = ['username']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','label','line1','line2','city','state','pincode','phone','is_default']