from django.contrib import admin
from .models import Entrepot, Zone, Rayon

@admin.register(Entrepot)
class EntrepotAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'adresse')
    search_fields = ('code', 'name')

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'entrepot')
    search_fields = ('code', 'name', 'entrepot__code')
    list_filter = ('entrepot',)
    autocomplete_fields = ['entrepot']

@admin.register(Rayon)
class RayonAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'zone', 'emplacement_limit', 'emplacement_used', 'emplacement_available_display')
    list_filter = ('zone',)
    search_fields = ('code', 'name', 'zone__code')
    autocomplete_fields = ['zone']

    def emplacement_available_display(self, obj):
        return obj.emplacement_available
    emplacement_available_display.short_description = "Emplacements disponibles"