from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ClientProfileViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'client-profiles', ClientProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]