from rest_framework import serializers
from .models import Entrepot, Zone, Rayon

class EntrepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrepot
        fields = ['id', 'code', 'name', 'adresse']

class ZoneSerializer(serializers.ModelSerializer):
    entrepot = serializers.StringRelatedField()

    class Meta:
        model = Zone
        fields = ['id', 'entrepot', 'code', 'name']

class RayonSerializer(serializers.ModelSerializer):
    zone = serializers.StringRelatedField()
    emplacement_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rayon
        fields = ['id', 'zone', 'code', 'name', 'emplacement_limit', 'emplacement_used', 'emplacement_available']