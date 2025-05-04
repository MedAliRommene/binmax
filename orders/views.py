from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Order, OrderItem, DeliverySlip, ClientOrderHistory, EmployeeDeliveryHistory
from .serializers import (
    CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer,
    DeliverySlipSerializer, ClientOrderHistorySerializer, EmployeeDeliveryHistorySerializer
)
from django.db import transaction

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(client=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        cart = self.get_object()
        delivery_type = request.data.get('delivery_type')
        delivery_address = request.data.get('delivery_address', cart.client.client_profile.adresse)

        if delivery_type not in ['DOMICILE', 'MAGASIN']:
            return Response({"error": "Type de livraison invalide"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(
                client=cart.client,
                delivery_type=delivery_type,
                delivery_address=delivery_address,
                total_amount=sum(item.product.price * item.quantity for item in cart.items.all())
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_order=item.product.price
                )
                item.product.vendus += item.quantity
                item.product.quantity -= item.quantity
                item.product.save()
            cart.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'CLIENT':
            return self.queryset.filter(client=self.request.user)
        return self.queryset

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({"error": "Statut invalide"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.role not in ['EMPLOYE', 'ADMIN']:
            return Response({"error": "Permission refusée"}, status=status.HTTP_403_FORBIDDEN)
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

class DeliverySlipViewSet(viewsets.ModelViewSet):
    queryset = DeliverySlip.objects.all()
    serializer_class = DeliverySlipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'EMPLOYE':
            return self.queryset.filter(employee=self.request.user)
        return self.queryset if self.request.user.is_staff else self.queryset.none()

class ClientOrderHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClientOrderHistory.objects.all()
    serializer_class = ClientOrderHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(client=self.request.user) if self.request.user.role == 'CLIENT' else self.queryset

class EmployeeDeliveryHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmployeeDeliveryHistory.objects.all()
    serializer_class = EmployeeDeliveryHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(employee=self.request.user) if self.request.user.role == 'EMPLOYE' else self.queryset