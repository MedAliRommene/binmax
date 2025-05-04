from rest_framework import serializers

from products.models import Product
from .models import Cart, CartItem, Order, OrderItem, DeliverySlip, ClientOrderHistory, EmployeeDeliveryHistory
from products.serializers import ProductSerializer, ProductImageSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    main_image = ProductImageSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'main_image']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['id', 'client', 'created_at', 'updated_at', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price_at_order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'client', 'created_at', 'delivery_type', 'delivery_address', 'total_amount', 'status', 'items']

class DeliverySlipSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    employee = serializers.StringRelatedField()

    class Meta:
        model = DeliverySlip
        fields = ['id', 'order', 'employee', 'created_at', 'status']

class ClientOrderHistorySerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    order = OrderSerializer(read_only=True)

    class Meta:
        model = ClientOrderHistory
        fields = ['id', 'client', 'order', 'created_at']

class EmployeeDeliveryHistorySerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()
    delivery_slip = DeliverySlipSerializer(read_only=True)

    class Meta:
        model = EmployeeDeliveryHistory
        fields = ['id', 'employee', 'delivery_slip', 'created_at']