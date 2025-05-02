from rest_framework import serializers
from .models import Palette
from products.serializers import ProductSerializer

class PaletteSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    nombre_produits_vendus = serializers.IntegerField(read_only=True)
    benefice = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Palette
        fields = [
            'id', 'reference', 'date_ajout', 'prix_achat', 'commentaire',
            'nombre_produits_vendus', 'benefice', 'products'
        ]