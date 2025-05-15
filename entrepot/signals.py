from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Rayon
from products.models import Product

@receiver(pre_save, sender=Rayon)
def validate_emplacement_limit(sender, instance, **kwargs):
    if instance.pk:  # Updating an existing Rayon
        old_rayon = sender.objects.get(pk=instance.pk)
        if instance.emplacement_limit != old_rayon.emplacement_limit:
            # Calculate total reste of all non-freed products in this Rayon
            total_reste = sum(
                product.reste for product in Product.objects.filter(
                    rayon=instance, emplacement_freed=False
                )
            )
            if instance.emplacement_limit < total_reste:
                raise ValueError(
                    f"La nouvelle limite d'emplacements ({instance.emplacement_limit}) est insuffisante. "
                    f"Les produits nécessitent {total_reste} emplacements."
                )