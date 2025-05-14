from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FournisseurViewSet, PaletteViewSet

router = DefaultRouter()
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'palettes', PaletteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]