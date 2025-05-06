from rest_framework import viewsets
from .models import Palette
from .serializers import PaletteSerializer

class PaletteViewSet(viewsets.ModelViewSet):
    queryset = Palette.objects.prefetch_related('products').select_related('fournisseur').all()
    serializer_class = PaletteSerializer

    def perform_create(self, serializer):
        palette = serializer.save()
        if not palette.reference:
            palette.reference = f"PAL-{palette.date_ajout.strftime('%y%m%d')}-{palette.id:04d}"
            palette.save(update_fields=['reference'])