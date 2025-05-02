from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaletteViewSet

router = DefaultRouter()
router.register(r'palettes', PaletteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]