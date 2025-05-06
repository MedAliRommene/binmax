from rest_framework import serializers
from .models import Palette, Fournisseur
from products.serializers import ProductSerializer

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = ['id', 'nom', 'contact', 'adresse']

class PaletteSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    nombre_produits_vendus = serializers.IntegerField(read_only=True)
    total_sold = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    benefice = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    fournisseur = FournisseurSerializer(read_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(
        queryset=Fournisseur.objects.all(), source='fournisseur', write_only=True, required=False
    )

    class Meta:
        model = Palette
        fields = [
            'id', 'reference', 'date_ajout', 'prix_achat', 'commentaire',
            'nombre_produits_vendus', 'total_sold', 'benefice', 'products',
            'fournisseur', 'fournisseur_id', 'categories'
        ]