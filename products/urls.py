from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ZoneViewSet, RayonViewSet, EmplacementViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'rayons', RayonViewSet)
router.register(r'emplacements', EmplacementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]