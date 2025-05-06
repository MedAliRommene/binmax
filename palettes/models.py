from django.db import models
from django.db.models import Sum
from decimal import Decimal

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom du Fournisseur")
    contact = models.CharField(max_length=100, blank=True, verbose_name="Contact")
    adresse = models.TextField(blank=True, verbose_name="Adresse")

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.nom

class Palette(models.Model):
    reference = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Référence")
    date_ajout = models.DateField(verbose_name="Date d'ajout")
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix d'achat")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True, related_name='palettes', verbose_name="Fournisseur")
    categories = models.CharField(max_length=200, blank=True, verbose_name="Catégories", help_text="Enter categories separated by commas")

    class Meta:
        verbose_name = "Palette"
        verbose_name_plural = "Palettes"
        ordering = ['-date_ajout']

    @property
    def nombre_produits_vendus(self):
        return self.products.aggregate(total=Sum('vendus'))['total'] or 0

    @property
    def total_sold(self):
        return sum(product.price * Decimal(product.vendus) for product in self.products.all()) or Decimal('0.00')

    @property
    def benefice(self):
        return self.total_sold - self.prix_achat

    def save(self, *args, **kwargs):
        if not self.reference:
            super().save(*args, **kwargs)
            self.reference = f"PAL-{self.date_ajout.strftime('%y%m%d')}-{self.id:04d}"
            super().save(update_fields=['reference'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.reference