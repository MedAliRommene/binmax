from django.contrib import admin
from django import forms
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
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
        if config and config.mode == 'daily':
            self.fields['price'].widget = forms.HiddenInput()
            self.fields['price'].required = False
        else:  # 'product' mode or no config yet
            self.fields['price'].widget = forms.TextInput()
            self.fields['price'].required = True

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

class PricingConfigurationForm(forms.ModelForm):
    class Meta:
        model = PricingConfiguration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use the form's instance data (if available) instead of fetching the existing config
        # On the "add" page, instance.mode will be None or the default ('product')
        # On POST, instance.mode will reflect the submitted data after binding
        mode = getattr(self.instance, 'mode', 'product')  # Default to 'product' if no instance
        if self.data.get('mode'):  # Check submitted data during POST
            mode = self.data.get('mode')

        if mode == 'product':
            for field in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False

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

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super().change_view(request, object_id, form_url, extra_context)
        except ValueError as e:
            if "Pas assez d'emplacements disponibles" in str(e):
                # Display an error message to the admin
                messages.error(
                    request,
                    f"Erreur : {str(e)}. Veuillez augmenter la limite d'emplacements du rayon ou réduire la quantité du produit."
                )
                # Re-render the form with the submitted data
                obj = self.get_object(request, object_id)
                form = self.get_form(request, obj)(data=request.POST, files=request.FILES, instance=obj)

                # Prepare the context with inline formsets
                context = self.get_changeform_initial_data(request)
                context.update({
                    'form': form,
                    'obj': obj,
                    'errors': form.errors,
                    'media': self.media + form.media,
                    'title': 'Modifier le produit',
                    'is_popup': '_popup' in request.GET,
                    'add': False,
                    'change': True,
                    'has_view_permission': self.has_view_permission(request, obj),
                    'has_add_permission': self.has_add_permission(request),
                    'has_change_permission': self.has_change_permission(request, obj),
                    'has_delete_permission': self.has_delete_permission(request, obj),
                    'opts': self.model._meta,
                    'original': obj,
                    'save_as': self.save_as,
                    'show_save': True,
                    'show_save_and_continue': True,
                })

                # Add inline formsets to the context
                inline_admin_formsets = self.get_inline_formsets(
                    request,
                    self.get_formsets_with_inlines(request, obj),
                    obj,
                    data=request.POST if request.method == 'POST' else None,
                    files=request.FILES if request.method == 'POST' else None,
                )
                context['inline_admin_formsets'] = inline_admin_formsets

                # Add media for inline formsets
                for inline_formset in inline_admin_formsets:
                    context['media'] = context['media'] + inline_formset.media

                return self.render_change_form(request, context, change=True, obj=obj)
            else:
                # Re-raise other ValueError exceptions
                raise

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
    form = PricingConfigurationForm
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