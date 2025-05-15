from django.contrib import admin
from django import forms
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from palettes.models import Palette
from entrepot.models import Zone, Rayon
from .models import Product, ProductImage, Category, PricingConfiguration
from django.db.models import F

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Aperçu"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        config = PricingConfiguration.get_config()
        if config.mode == 'daily':
            self.fields['price'].widget = forms.HiddenInput()
            self.fields['price'].required = False

        palette_id = self.request.GET.get('palette') if self.request else None
        if palette_id:
            try:
                palette = Palette.objects.get(pk=palette_id)
            except Palette.DoesNotExist:
                pass
            else:
                self.fields['palette'].initial = palette
                self.fields['palette'].widget = forms.HiddenInput()
                self.fields['category'].queryset = Category.objects.filter(entrepot=palette.entrepot)
                self.fields['zone'].queryset = Zone.objects.filter(entrepot=palette.entrepot)
                self.fields['rayon'].queryset = Rayon.objects.filter(
                    zone__entrepot=palette.entrepot,
                    emplacement_used__lt=F('emplacement_limit')
                )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline]
    list_display = ('reference', 'name', 'category', 'price', 'vendus', 'reste')
    list_filter = ('palette__entrepot', 'category')
    search_fields = ('reference', 'name')
    readonly_fields = ('reference', 'reste', 'palette_link')
    fieldsets = (
        ('Général', {'fields': ('name', 'description', 'palette', 'palette_link')}),
        ('Logistique', {'fields': ('category', 'zone', 'rayon')}),
        ('Stock', {'fields': ('price', 'quantity', 'vendus', 'reste')}),
    )

    def palette_link(self, obj):
        if not obj.palette:
            return "-"
        url = reverse('admin:palettes_palette_change', args=[obj.palette.id])
        return format_html('<a href="{}">{}</a>', url, obj.palette)
    palette_link.short_description = "Palette Associée"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('palette', 'category', 'zone', 'rayon')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def response_post_save_add(self, request, obj):
        if '_continue' in request.POST:
            return super().response_post_save_add(request, obj)
        return redirect(reverse('admin:palettes_palette_changelist'))

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'entrepot')
    search_fields = ('code', 'name', 'entrepot__code')
    list_filter = ('entrepot',)
    autocomplete_fields = ['entrepot']

@admin.register(PricingConfiguration)
class PricingConfigurationAdmin(admin.ModelAdmin):
    list_display = ('mode', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi')

    def has_add_permission(self, request):
        return not PricingConfiguration.objects.exists()

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'GET' and PricingConfiguration.objects.exists():
            pc = PricingConfiguration.objects.first()
            return redirect(reverse('admin:products_pricingconfiguration_change', args=[pc.pk]))
        return super().add_view(request, form_url, extra_context)

    class Media:
        js = ('js/pricing_mode.js',)