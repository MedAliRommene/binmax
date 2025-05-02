from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def generate_product_reference(sender, instance, created, **kwargs):
    if created and not instance.reference:
        palette_ref = instance.palette.reference.replace("PAL-", "")
        instance.reference = (
            f"PAL-{palette_ref}-"
            f"{instance.category.code}-"
            f"{instance.emplacement.rayon.zone.code}-"
            f"{instance.emplacement.rayon.code}-"
            f"{instance.emplacement.code}-"
            f"{Product.objects.filter(palette=instance.palette).count():04d}"
        )
        instance.save()