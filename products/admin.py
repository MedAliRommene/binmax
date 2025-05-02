from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Zone, Rayon, Emplacement, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Aperçu"

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ('name', 'category', 'emplacement', 'price', 'quantity', 'vendus', 'description')
    autocomplete_fields = ['category', 'emplacement']
    readonly_fields = ('reference',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('reference', 'name', 'palette', 'category', 'emplacement', 'price', 'quantity', 'vendus', 'reste')
    search_fields = ('reference', 'name')
    list_filter = ('palette', 'category', 'emplacement__rayon__zone')
    readonly_fields = ('reference',)
    fieldsets = (
        ('Informations Générales', {
            'fields': ('reference', 'name', 'description', 'palette')
        }),
        ('Stockage', {
            'fields': ('category', 'emplacement')
        }),
        ('Inventaire', {
            'fields': ('price', 'quantity', 'vendus')
        }),
    )
    autocomplete_fields = ['palette', 'category', 'emplacement']

    def reste(self, obj):
        return obj.reste
    reste.short_description = "Reste à vendre"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Rayon)
class RayonAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'zone', 'emplacement_count')
    list_filter = ('zone',)
    search_fields = ('code', 'name', 'zone__code')
    autocomplete_fields = ['zone']

@admin.register(Emplacement)
class EmplacementAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'rayon')
    list_filter = ('rayon__zone',)
    search_fields = ('code', 'name', 'rayon__code')
    autocomplete_fields = ['rayon']