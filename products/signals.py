from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from model_utils import FieldTracker
from .models import PricingConfiguration, Product
from decimal import Decimal

@receiver(post_save, sender=Product)
def generate_product_reference(sender, instance, created, **kwargs):
    if created and not instance.reference:
        palette_ref = instance.palette.reference.replace("PAL-", "")
        instance.reference = (
            f"{instance.rayon.zone.entrepot.code}-"
            f"PAL-{palette_ref}-"
            f"{instance.category.code}-"
            f"{instance.rayon.zone.code}-"
            f"{instance.rayon.code}-"
            f"{Product.objects.filter(palette=instance.palette).count():04d}"
        )
        # Update the reference without calling save() to avoid recursion
        Product.objects.filter(pk=instance.pk).update(reference=instance.reference)

# Add tracker to PricingConfiguration
PricingConfiguration._tracker = FieldTracker(fields=['mode'])

@receiver(pre_save, sender=PricingConfiguration)
def pricing_mode_pre_save(sender, instance, **kwargs):
    # Only fetch the old instance if this is an update (pk exists)
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            instance._old_mode = old.mode
        except sender.DoesNotExist:
            instance._old_mode = None
    else:
        # For new instances (creation), set _old_mode to None
        instance._old_mode = None

@receiver(post_save, sender=PricingConfiguration)
def update_product_prices_on_mode_change(sender, instance, created, **kwargs):
    old_mode = getattr(instance, '_old_mode', None)
    new_mode = instance.mode
    if not created and old_mode != new_mode:
        if new_mode == 'daily':
            products = Product.objects.all()
            for p in products:
                day_field = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'][p.date_creation.weekday()]
                daily_price = getattr(instance, day_field) or p.price_at_creation or Decimal('0.00')
                p.price = daily_price
                p.save(update_fields=['price'])
        else:  # 'product' mode
            products = Product.objects.all()
            for p in products:
                p.price = p.price_at_creation or p.price or Decimal('0.00')
                p.save(update_fields=['price'])