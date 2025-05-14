from rest_framework import serializers

from entrepot.models import Entrepot
from .models import Palette, Fournisseur
from products.serializers import ProductSerializer
from entrepot.serializers import EntrepotSerializer

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
    entrepot = EntrepotSerializer(read_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(
        queryset=Fournisseur.objects.all(), source='fournisseur', write_only=True, required=False
    )
    entrepot_id = serializers.PrimaryKeyRelatedField(
        queryset=Entrepot.objects.all(), source='entrepot', write_only=True, required=True
    )

    class Meta:
        model = Palette
        fields = [
            'id', 'reference', 'entrepot', 'entrepot_id', 'date_ajout', 'prix_achat', 'commentaire',
            'nombre_produits_vendus', 'total_sold', 'benefice', 'products',
            'fournisseur', 'fournisseur_id', 'categories'
        ]