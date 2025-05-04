from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, DeliverySlip, ClientOrderHistory, EmployeeDeliveryHistory
from products.models import Product, ProductImage
from users.models import CustomUser

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    main_image = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all(), allow_null=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'main_image']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='CLIENT'))

    class Meta:
        model = Cart
        fields = ['id', 'client', 'created_at', 'updated_at', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='CLIENT'))
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False)

    class Meta:
        model = Order
        fields = ['id', 'client', 'created_at', 'delivery_type', 'delivery_address', 'total_amount', 'status', 'items']

class DeliverySlipSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='EMPLOYE'), allow_null=True)
    status = serializers.ChoiceField(choices=DeliverySlip.STATUS_CHOICES)

    class Meta:
        model = DeliverySlip
        fields = ['id', 'order', 'employee', 'created_at', 'status']

class ClientOrderHistorySerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='CLIENT'))
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = ClientOrderHistory
        fields = ['id', 'client', 'order', 'created_at']

class EmployeeDeliveryHistorySerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='EMPLOYE'))
    delivery_slip = serializers.PrimaryKeyRelatedField(queryset=DeliverySlip.objects.all())

    class Meta:
        model = EmployeeDeliveryHistory
        fields = ['id', 'employee', 'delivery_slip', 'created_at']