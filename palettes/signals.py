from django.db.models.signals import post_delete
from django.dispatch import receiver
from products.models import Product

@receiver(post_delete, sender=Product)
def free_emplacement_on_product_delete(sender, instance, **kwargs):
    if instance.rayon:
        print(f"Deleting product {instance.reference}: Freeing {instance.reste} emplacements")
        instance.rayon.emplacement_used = max(0, instance.rayon.emplacement_used - instance.reste)
        print(f"After deletion, emplacement_used is now {instance.rayon.emplacement_used}")
        instance.rayon.save(update_fields=['emplacement_used'])