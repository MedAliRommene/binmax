from rest_framework import viewsets
from .models import Palette, Fournisseur
from .serializers import PaletteSerializer, FournisseurSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class PaletteViewSet(viewsets.ModelViewSet):
    queryset = Palette.objects.prefetch_related('products').select_related('fournisseur', 'entrepot').all()
    serializer_class = PaletteSerializer

    def perform_create(self, serializer):
        palette = serializer.save()
        if not palette.reference:
            palette.reference = f"PAL-{palette.date_ajout.strftime('%y%m%d')}-{palette.id:04d}"
            palette.save(update_fields=['reference'])