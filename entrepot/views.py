from rest_framework import viewsets
from .models import Entrepot, Zone, Rayon
from .serializers import EntrepotSerializer, ZoneSerializer, RayonSerializer

class EntrepotViewSet(viewsets.ModelViewSet):
    queryset = Entrepot.objects.all()
    serializer_class = EntrepotSerializer

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class RayonViewSet(viewsets.ModelViewSet):
    queryset = Rayon.objects.all()
    serializer_class = RayonSerializer