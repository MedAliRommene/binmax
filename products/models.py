from django.db import models
from django.db.models import F, Max
from model_utils import FieldTracker

class Category(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

class Zone(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"
        ordering = ['code']

    def __str__(self):
        return f"ZONE-{self.code}"

class Rayon(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name='rayons', verbose_name="Zone")
    code = models.CharField(max_length=10, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")
    emplacement_count = models.PositiveIntegerField(default=0, verbose_name="Nombre d'emplacements")

    class Meta:
        unique_together = ('zone', 'code')
        verbose_name = "Rayon"
        verbose_name_plural = "Rayons"
        ordering = ['zone__code', 'code']

    def __str__(self):
        return f"{self.zone.code}-RAYON-{self.code}"

class Emplacement(models.Model):
    rayon = models.ForeignKey(Rayon, on_delete=models.PROTECT, related_name='emplacements', verbose_name="Rayon")
    code = models.CharField(max_length=10, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        unique_together = ('rayon', 'code')
        verbose_name = "Emplacement"
        verbose_name_plural = "Emplacements"
        ordering = ['rayon__zone__code', 'rayon__code', 'code']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.rayon.emplacement_count = self.rayon.emplacements.count()
        self.rayon.save(update_fields=['emplacement_count'])

    def __str__(self):
        return f"{self.rayon.zone.code}-{self.rayon.code}-EMP-{self.code}"

class Product(models.Model):
    reference = models.CharField(max_length=100, unique=True, editable=False, verbose_name="Référence")
    palette = models.ForeignKey('palettes.Palette', on_delete=models.CASCADE, related_name='products', verbose_name="Palette")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Catégorie")
    emplacement = models.ForeignKey(Emplacement, on_delete=models.PROTECT, verbose_name="Emplacement")
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    vendus = models.PositiveIntegerField(default=0, verbose_name="Vendus")
    tracker = FieldTracker(fields=['vendus'])

    @property
    def reste(self):
        return self.quantity - self.vendus

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['reference']

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