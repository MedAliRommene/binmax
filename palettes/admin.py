from django.contrib import admin
from django.utils.html import format_html
from django import forms
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Palette, Fournisseur
from products.models import Product, ProductImage, PricingConfiguration, Category
from entrepot.models import Zone, Rayon
from django.db.models import F

class ProductImageInline(NestedTabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url) if obj.image else "-"
    image_preview.short_description = "Aperçu"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        config = PricingConfiguration.get_config()
        if config.mode == 'daily':
            self.fields['price'].widget = forms.HiddenInput()
            self.fields['price'].required = False
        
        # Check if we're in the admin context with a Palette instance
        if hasattr(self, 'request') and hasattr(self.request, '_palette_') and self.request._palette_:
            palette = self.request._palette_
            self.fields['category'].queryset = Category.objects.filter(entrepot=palette.entrepot)
            self.fields['zone'].queryset = Zone.objects.filter(entrepot=palette.entrepot)
            self.fields['rayon'].queryset = Rayon.objects.filter(
                zone__entrepot=palette.entrepot, emplacement_used__lt=F('emplacement_limit')
            )

class CustomProductInline(NestedTabularInline):
    model = Product
    form = ProductForm
    extra = 1
    fields = (
        'reference', 'name', 'category', 'zone', 'rayon', 'price', 'quantity', 
        'vendus', 'reste_display', 'description', 'current_price_display'
    )
    autocomplete_fields = ['category', 'zone', 'rayon']
    readonly_fields = ('reference', 'reste_display', 'current_price_display')
    inlines = [ProductImageInline]

    def get_formset(self, request, obj=None, **kwargs):
        # Pass the request to the form
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.request = request
        return formset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['category', 'zone', 'rayon'] and hasattr(request, '_palette_'):
            if db_field.name == "category":
                kwargs["queryset"] = Category.objects.filter(entrepot=request._palette_.entrepot)
            elif db_field.name == "zone":
                kwargs["queryset"] = Zone.objects.filter(entrepot=request._palette_.entrepot)
            elif db_field.name == "rayon":
                kwargs["queryset"] = Rayon.objects.filter(
                    zone__entrepot=request._palette_.entrepot, emplacement_used__lt=F('emplacement_limit')
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def reste_display(self, obj):
        try:
            return obj.reste
        except TypeError:
            return "-"
    reste_display.short_description = "Reste"

    def current_price_display(self, obj):
        try:
            config = PricingConfiguration.get_config()
            if config.mode == 'daily':
                return f"{obj.prix_effectif} € (Journalier)"
            return f"{obj.prix_effectif} € (Produit)"
        except AttributeError:
            return "-"
    current_price_display.short_description = "Prix Actuel"

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse')
    search_fields = ('nom',)

@admin.register(Palette)
class PaletteAdmin(NestedModelAdmin):
    inlines = [CustomProductInline]
    list_display = (
        'reference', 'entrepot', 'date_ajout', 'prix_achat', 'fournisseur', 'categories',
        'nombre_produits_vendus', 'total_sold_display', 'benefice_display'
    )
    search_fields = ('reference', 'fournisseur__nom', 'categories')
    list_filter = ('date_ajout', 'fournisseur', 'entrepot')
    readonly_fields = ('reference', 'nombre_produits_vendus', 'total_sold_display', 'benefice_display')
    fieldsets = (
        ('Informations Générales', {
            'fields': ('reference', 'entrepot', 'date_ajout', 'prix_achat', 'commentaire')
        }),
        ('Fournisseur et Catégories', {
            'fields': ('fournisseur', 'categories')
        }),
    )
    autocomplete_fields = ['fournisseur', 'entrepot']

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