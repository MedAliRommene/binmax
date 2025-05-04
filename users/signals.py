from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ClientProfile

@receiver(post_save, sender=CustomUser)
def create_client_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'CLIENT':
        ClientProfile.objects.create(
            user=instance,
            nom=instance.last_name or "Nom",
            prenom=instance.first_name or "Prénom",
            adresse="Adresse par défaut",
            solde_de_credit=0.00
        )