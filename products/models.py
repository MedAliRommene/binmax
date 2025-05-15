from django.db import models
from django.db.models import F
from decimal import Decimal
from model_utils import FieldTracker
from entrepot.models import Entrepot, Zone, Rayon
from palettes.models import Palette

class Category(models.Model):
    entrepot = models.ForeignKey(Entrepot, on_delete=models.PROTECT, related_name='categories', verbose_name="Entrepôt")
    code = models.CharField(max_length=10, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        unique_together = ('entrepot', 'code')
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['entrepot__code', 'code']

    def __str__(self):
        return f"{self.entrepot.code}-{self.code}"

class Product(models.Model):
    reference = models.CharField(max_length=100, unique=True, editable=False, verbose_name="Référence")
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE, related_name='products', verbose_name="Palette")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Catégorie")
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, verbose_name="Zone")
    rayon = models.ForeignKey(Rayon, on_delete=models.PROTECT, verbose_name="Rayon")
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Prix"
    )
    price_at_creation = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Prix à la création"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantité", default=0)
    vendus = models.PositiveIntegerField(default=0, verbose_name="Vendus")
    tracker = FieldTracker(fields=['vendus', 'quantity'])
    emplacement_freed = models.BooleanField(default=False, verbose_name="Emplacement libéré", editable=False)

    @property
    def prix_effectif(self):
        config = PricingConfiguration.get_config()
        if config.mode == 'daily':
            from django.utils import timezone
            jour = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'][self.date_creation.weekday()]
            return getattr(config, jour, Decimal('0.00')) or self.price_at_creation or Decimal('0.00')
        return self.price_at_creation or Decimal('0.00')

    @property
    def reste(self):
        return self.quantity - self.vendus

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['reference']

    def save(self, *args, **kwargs):
        if not self.palette_id:
            raise ValueError("Une palette doit être associée au produit")

        # Fetch the previous state from the database if the product exists
        old_reste = 0
        if self.pk:
            try:
                old_product = Product.objects.get(pk=self.pk)
                old_reste = old_product.quantity - old_product.vendus
                print(f"Previous state: quantity={old_product.quantity}, vendus={old_product.vendus}, old_reste={old_reste}")
            except Product.DoesNotExist:
                old_reste = 0

        # Calculate new reste
        new_reste = self.quantity - self.vendus
        print(f"New state: quantity={self.quantity}, vendus={self.vendus}, new_reste={new_reste}")

        # Handle creation
        if self.pk is None:
            if self.rayon.emplacement_available < self.quantity:
                raise ValueError(f"Pas assez d'emplacements disponibles : {self.rayon.emplacement_available} disponibles, {self.quantity} nécessaires")
            self.rayon.emplacement_used += self.quantity
            print(f"Creating product: Adding {self.quantity} to emplacement_used, now {self.rayon.emplacement_used}")
            self.rayon.save(update_fields=['emplacement_used'])
            if self.price and not self.price_at_creation:
                self.price_at_creation = self.price

        # Save the product
        super().save(*args, **kwargs)

        # Handle reste changes after saving
        if self.pk:  # Only for updates
            reste_change = new_reste - old_reste
            print(f"Reste change: {reste_change} (from {old_reste} to {new_reste})")
            if reste_change != 0:  # Reste has changed
                if new_reste == 0:  # Reste reached 0
                    self.rayon.emplacement_used = max(0, self.rayon.emplacement_used - old_reste)
                    self.emplacement_freed = True
                    print(f"Reste reached 0: Reducing emplacement_used by {old_reste}, now {self.rayon.emplacement_used}")
                else:  # General case: reste changed
                    effective_available = self.rayon.emplacement_available - reste_change
                    if effective_available < 0:
                        raise ValueError(f"Pas assez d'emplacements disponibles : {effective_available + reste_change} disponibles, {new_reste} nécessaires")
                    self.rayon.emplacement_used += reste_change
                    print(f"Reste changed: Adjusting emplacement_used by {reste_change}, now {self.rayon.emplacement_used}")
                    if self.emplacement_freed and new_reste > 0:  # Reset flag if reste becomes non-zero
                        self.emplacement_freed = False
                        super().save(update_fields=['emplacement_freed'])
                self.rayon.save(update_fields=['emplacement_used'])

    def __str__(self):
        return f"{self.reference} - {self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="Produit")
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    is_main = models.BooleanField(default=False, verbose_name="Image principale")

    class Meta:
        verbose_name = "Image de produit"
        verbose_name_plural = "Images de produit"
        ordering = ['-is_main']

    def __str__(self):
        return f"Image {self.id} - {self.product.name}"

class PricingConfiguration(models.Model):
    MODE_CHOICES = [
        ('daily', 'Prix journalier'),
        ('product', 'Prix par produit')
    ]
    
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='product')
    lundi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    mardi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    mercredi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    jeudi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    vendredi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    samedi = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Configuration des Prix"
        verbose_name_plural = "Configurations des Prix"

    def save(self, *args, **kwargs):
        self.id = 1  # Singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        return cls.objects.get_or_create(id=1)[0]
    