from django.db.models.signals import post_delete
from django.dispatch import receiver
from products.models import Product
from entrepot.models import Rayon

@receiver(post_delete, sender=Product)
def free_emplacement_on_product_delete(sender, instance, **kwargs):
    if instance.rayon:
        instance.rayon.emplacement_used -= 1
        instance.rayon.save(update_fields=['emplacement_used'])