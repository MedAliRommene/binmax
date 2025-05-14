from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from .models import Palette, Fournisseur
from products.models import Product, ProductImage, Category
from entrepot.models import Zone, Rayon
from django.db.models import F

@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse')
    search_fields = ('nom',)

class PaletteForm(forms.ModelForm):
    nombre_produits = forms.IntegerField(
        label="Nombre de produits",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Palette
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['nombre_produits'] = self.instance.products.count()

@admin.register(Palette)
class PaletteAdmin(admin.ModelAdmin):
    form = PaletteForm
    list_display = (
        'reference', 'entrepot', 'date_ajout', 'prix_achat',
        'fournisseur', 'produits_link', 'total_vendu', 'benefice'
    )
    readonly_fields = ('reference', 'total_vendu', 'benefice', 'produits_link')
    fieldsets = (
        ('Informations Générales', {
            'fields': ('reference', 'entrepot', 'date_ajout', 'prix_achat', 'commentaire')
        }),
        ('Fournisseur', {
            'fields': ('fournisseur', 'categories', 'nombre_produits')
        }),
        ('Statistiques', {
            'fields': ('produits_link', 'total_vendu', 'benefice')
        }),
    )
    autocomplete_fields = ['fournisseur', 'entrepot']

    def produits_link(self, obj):
        count = obj.products.count()
        add_url = reverse('admin:products_product_add') + f'?palette={obj.id}'
        list_url = reverse('admin:products_product_changelist') + f'?palette__id__exact={obj.id}'
        return format_html(
            '<a class="button" href="{}">+ Ajouter</a> '
            '<a class="button" href="{}">{} Produits</a>',
            add_url, list_url, count
        )
    produits_link.short_description = "Produits"

    def total_vendu(self, obj):
        total = sum(p.prix_effectif * p.vendus for p in obj.products.all())
        return f"{total:.2f} €"
    total_vendu.short_description = "Total Vendu"

    def benefice(self, obj):
        return f"{float(self.total_vendu(obj).split(' ')[0]) - float(obj.prix_achat):.2f} €"
    benefice.short_description = "Bénéfice"
    
    def response_add(self, request, obj, post_url_continue=None):
        # Rediriger vers l'ajout de produit après création de palette
        if '_add_another' in request.POST:
            return redirect(reverse('admin:products_product_add') + f'?palette={obj.id}')
        return super().response_add(request, obj, post_url_continue)

    class Media:
        css = {
            'all': ('css/palette_admin.css',)
        }