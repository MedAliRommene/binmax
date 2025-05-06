from django.contrib import admin
from django.utils.html import format_html
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Palette, Fournisseur
from products.models import Product, ProductImage

class ProductImageInline(NestedTabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Aperçu"

class CustomProductInline(NestedTabularInline):
    model = Product
    extra = 1
    fields = ('name', 'category', 'emplacement', 'price', 'quantity', 'vendus', 'description', 'reference', 'palette')
    autocomplete_fields = ['category', 'emplacement']
    readonly_fields = ('reference', 'palette')  # Make palette readonly in the inline
    inlines = [ProductImageInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "palette" and hasattr(request, '_palette_'):
            kwargs["queryset"] = Palette.objects.filter(id=request._palette_.id)
            kwargs["initial"] = request._palette_
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse')
    search_fields = ('nom',)

@admin.register(Palette)
class PaletteAdmin(NestedModelAdmin):
    inlines = [CustomProductInline]
    list_display = (
        'reference', 'date_ajout', 'prix_achat', 'fournisseur', 'categories',
        'nombre_produits_vendus', 'total_sold_display', 'benefice_display'
    )
    search_fields = ('reference', 'fournisseur__nom', 'categories')
    list_filter = ('date_ajout', 'fournisseur')
    readonly_fields = ('reference', 'nombre_produits_vendus', 'total_sold_display', 'benefice_display')
    fieldsets = (
        ('Informations Générales', {
            'fields': ('reference', 'date_ajout', 'prix_achat', 'commentaire')
        }),
        ('Fournisseur et Catégories', {
            'fields': ('fournisseur', 'categories')
        }),
    )
    autocomplete_fields = ['fournisseur']

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            request._palette_ = obj
        return super().get_form(request, obj, **kwargs)

    def total_sold_display(self, obj):
        return f"{obj.total_sold:.2f} €" if obj.total_sold else "0.00 €"
    total_sold_display.short_description = "Total Vendu"

    def benefice_display(self, obj):
        return f"{obj.benefice:.2f} €" if obj.benefice else "0.00 €"
    benefice_display.short_description = "Bénéfice"

    def nombre_produits_vendus(self, obj):
        return obj.nombre_produits_vendus
    nombre_produits_vendus.short_description = "Produits Vendus"