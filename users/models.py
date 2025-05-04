from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class CustomUser(AbstractUser):
    ROLES = [
        ('CLIENT', 'Client'),
        ('LIVREUR', 'Livreur'),
        ('EMPLOYE', 'Employé'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='CLIENT', verbose_name="Rôle")
    location = models.CharField(max_length=100, blank=True, verbose_name="Lieu")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groupes'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='permissions utilisateur'
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['username']

    def __str__(self):
        return self.username

class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='client_profile', verbose_name="Utilisateur")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    adresse = models.TextField(verbose_name="Adresse")
    solde_de_credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
        verbose_name="Solde de crédit"
    )

    class Meta:
        verbose_name = "Profil Client"
        verbose_name_plural = "Profils Clients"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.user.username})"