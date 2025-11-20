
from rest_framework import serializers
from .models import Category, SubCategory, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
fields = ['id','name','slug']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id','category','name','slug']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
fields = ['id','title','slug','description','price','sale_price','stock','subcategory']