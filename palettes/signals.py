from django.db.models.signals import post_delete
from django.dispatch import receiver
from products.models import Product


@receiver(post_delete, sender=Product)
def free_emplacement_on_product_delete(sender, instance, **kwargs):
    if instance.rayon and not instance.emplacement_freed:
        print(
            f"Freeing {instance.quantity} emplacements for product {instance.reference}"
        )
        instance.rayon.emplacement_used = max(
            0, instance.rayon.emplacement_used - instance.quantity
        )
        instance.rayon.save(update_fields=["emplacement_used"])
