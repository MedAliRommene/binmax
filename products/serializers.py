from rest_framework import serializers
from .models import Product, Category, Zone, Rayon, Emplacement, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    palette = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    emplacement = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id', 'reference', 'palette', 'category', 'emplacement',
            'name', 'description', 'price', 'quantity', 'vendus', 'reste'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'code', 'name']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'code', 'name']

class RayonSerializer(serializers.ModelSerializer):
    zone = serializers.StringRelatedField()

    class Meta:
        model = Rayon
        fields = ['id', 'zone', 'code', 'name', 'emplacement_count']

class EmplacementSerializer(serializers.ModelSerializer):
    rayon = serializers.StringRelatedField()

    class Meta:
        model = Emplacement
        fields = ['id', 'rayon', 'code', 'name']