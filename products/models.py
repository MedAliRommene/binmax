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
    date_creation = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantité", default=0)
    vendus = models.PositiveIntegerField(default=0, verbose_name="Vendus")
    tracker = FieldTracker(fields=['vendus'])

    @property
    def prix_effectif(self):
        config = PricingConfiguration.get_config()
        if config.mode == 'daily':
            jour = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'][self.date_creation.weekday()]
            return getattr(config, jour) or Decimal('0.00')
        return self.price or Decimal('0.00')

    @property
    def reste(self):
        return self.quantity - self.vendus

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['reference']

    def save(self, *args, **kwargs):
        # Toujours requérir une palette
        if not self.palette_id:
            raise ValueError("Une palette doit être associée au produit")
        # Gestion des emplacements
        if self.pk is None:
            if self.rayon.emplacement_available <= 0:
                raise ValueError("Aucun emplacement disponible")
            self.rayon.emplacement_used += 1
            self.rayon.save(update_fields=['emplacement_used'])
        super().save(*args, **kwargs)
        # Libérer l’emplacement quand tout est vendu
        if self.reste == 0 and self.tracker.has_changed('vendus'):
            self.rayon.emplacement_used -= 1
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
        verbose_name_plural = "Configuration des Prix"

    def save(self, *args, **kwargs):
        self.id = 1  # Singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        return cls.objects.get_or_create(id=1)[0]