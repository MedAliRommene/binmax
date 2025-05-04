from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ClientProfile

class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False
    verbose_name_plural = "Profil Client"
    fields = ('nom', 'prenom', 'adresse', 'solde_de_credit')
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [ClientProfileInline]
    list_display = ('username', 'email', 'role', 'location', 'is_staff', 'solde_de_credit')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'role', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'location'),
        }),
    )
    ordering = ('username',)

    def solde_de_credit(self, obj):
        if obj.role == 'CLIENT' and hasattr(obj, 'client_profile'):
            return f"{obj.client_profile.solde_de_credit:.2f} €"
        return "-"
    solde_de_credit.short_description = "Solde de crédit"

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'prenom', 'adresse', 'solde_de_credit')
    search_fields = ('user__username', 'nom', 'prenom', 'adresse')
    list_filter = ('user__role',)
    fields = ('user', 'nom', 'prenom', 'adresse', 'solde_de_credit')
    readonly_fields = ('user',)