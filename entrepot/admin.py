from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Entrepot, Zone, Rayon

@admin.register(Entrepot)
class EntrepotAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'adresse', 'total_emplacements_disponibles', 'liste_zones', 'liste_rayons')
    search_fields = ('code', 'name')

    def total_emplacements_disponibles(self, obj):
        total = sum(rayon.emplacement_available for rayon in Rayon.objects.filter(zone__entrepot=obj))
        return total
    total_emplacements_disponibles.short_description = "Emplacements disponibles"

    def liste_zones(self, obj):
        url = reverse('admin:entrepot_zone_changelist') + f'?entrepot__id__exact={obj.id}'
        return format_html('<a href="{}">Liste des Zones</a>', url)
    liste_zones.short_description = "Zones"

    def liste_rayons(self, obj):
        url = reverse('admin:entrepot_rayon_changelist') + f'?zone__entrepot__id__exact={obj.id}'
        return format_html('<a href="{}">Liste des Rayons</a>', url)
    liste_rayons.short_description = "Rayons"

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'entrepot')
    search_fields = ('code', 'name', 'entrepot__code')
    list_filter = ('entrepot',)
    autocomplete_fields = ['entrepot']

@admin.register(Rayon)
class RayonAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'zone', 'emplacement_limit', 'emplacement_used', 'emplacement_available_display')
    list_filter = ('zone', 'zone__entrepot')
    search_fields = ('code', 'name', 'zone__code')
    autocomplete_fields = ['zone']

    def emplacement_available_display(self, obj):
        return obj.emplacement_available
    emplacement_available_display.short_description = "Emplacements disponibles"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('zone__entrepot')