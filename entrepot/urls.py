from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntrepotViewSet, ZoneViewSet, RayonViewSet

router = DefaultRouter()
router.register(r'entrepots', EntrepotViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'rayons', RayonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]