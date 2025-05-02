from django.contrib import admin
from django.utils.html import format_html
from .models import Palette
from products.admin import ProductInline

@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = (
        'reference', 'date_ajout', 'prix_achat',
        'nombre_produits_vendus', 'benefice_display'
    )
    search_fields = ('reference',)
    list_filter = ('date_ajout',)
    fields = ('date_ajout', 'prix_achat', 'commentaire')
    readonly_fields = ('reference',)

    def benefice_display(self, obj):
        return f"{obj.benefice:.2f} €"
    benefice_display.short_description = "Bénéfice"

    def nombre_produits_vendus(self, obj):
        return obj.nombre_produits_vendus
    nombre_produits_vendus.short_description = "Produits vendus"