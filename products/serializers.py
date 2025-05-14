from rest_framework import serializers
from .models import Category, Product, ProductImage, PricingConfiguration
from palettes.models import Palette
from entrepot.serializers import EntrepotSerializer

class CategorySerializer(serializers.ModelSerializer):
    entrepot = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = ['id', 'entrepot', 'code', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    palette = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    zone = serializers.StringRelatedField()
    rayon = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 'reference', 'palette', 'category', 'zone', 'rayon',
            'name', 'description', 'price', 'quantity', 'vendus', 'reste'
        ]