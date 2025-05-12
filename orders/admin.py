from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem, DeliverySlip, ClientOrderHistory, EmployeeDeliveryHistory

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('product', 'quantity', 'main_image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.main_image.image.url)
        return "-"
    image_preview.short_description = "Aperçu"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('client', 'created_at', 'updated_at', 'item_count')
    search_fields = ('client__username',)
    list_filter = ('created_at',)

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Nombre d'articles"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price_at_order')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'client', 'created_at', 'delivery_type', 'delivery_address', 'total_amount', 'status', 'delivery_slip_status')
    search_fields = ('client__username', 'delivery_address')
    list_filter = ('delivery_type', 'status', 'created_at')
    readonly_fields = ('created_at', 'total_amount')
    fields = ('client', 'delivery_type', 'delivery_address', 'total_amount', 'status', 'created_at')

    def delivery_slip_status(self, obj):
        return obj.delivery_slip.status if hasattr(obj, 'delivery_slip') else "-"
    delivery_slip_status.short_description = "Statut du bon de commande"

@admin.register(DeliverySlip)
class DeliverySlipAdmin(admin.ModelAdmin):
    list_display = ('order', 'employee', 'created_at', 'status', 'products_list')
    search_fields = ('order__id', 'employee__username')
    list_filter = ('status', 'created_at')
    fields = ('order', 'employee', 'status', 'created_at')
    readonly_fields = ('order', 'created_at')

    def products_list(self, obj):
        items = obj.order.items.all()
        return format_html('<br>'.join(
            f"{item.quantity} x {item.product.name} (Ref: {item.product.reference})"
            for item in items
        ))
    products_list.short_description = "Produits"

@admin.register(ClientOrderHistory)
class ClientOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'order', 'created_at')
    search_fields = ('client__username', 'order__id')
    list_filter = ('created_at',)
    readonly_fields = ('client', 'order', 'created_at')

@admin.register(EmployeeDeliveryHistory)
class EmployeeDeliveryHistoryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'delivery_slip', 'created_at')
    search_fields = ('employee__username', 'delivery_slip__order__id')
    list_filter = ('created_at',)
    readonly_fields = ('employee', 'delivery_slip', 'created_at')