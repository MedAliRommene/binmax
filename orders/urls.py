from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet, OrderViewSet, DeliverySlipViewSet,
    ClientOrderHistoryViewSet, EmployeeDeliveryHistoryViewSet
)

router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'delivery-slips', DeliverySlipViewSet)
router.register(r'client-order-history', ClientOrderHistoryViewSet)
router.register(r'employee-delivery-history', EmployeeDeliveryHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]