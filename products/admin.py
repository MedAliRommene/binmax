from django.contrib import admin
from django import forms
from .models import Category, PricingConfiguration

class PricingConfigurationForm(forms.ModelForm):
    class Meta:
        model = PricingConfiguration
        fields = '__all__'
        widgets = {
            'mode': forms.Select(attrs={'onchange': "this.form.submit();"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.mode == 'daily':
            for field in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']:
                self.fields[field].required = True
        else:
            for field in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']:
                self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        mode = cleaned_data.get('mode')
        if mode == 'daily':
            for field in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']:
                if not cleaned_data.get(field):
                    self.add_error(field, "Ce champ est obligatoire en mode journalier.")
        return cleaned_data

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

    class Media:
        js = ('js/pricing_mode.js',)