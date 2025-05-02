from django.db import models
from django.db.models import Sum

class Palette(models.Model):
    reference = models.CharField(max_length=20, unique=True, editable=False, verbose_name="Référence")
    date_ajout = models.DateField(verbose_name="Date d'ajout")
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix d'achat")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")

    class Meta:
        verbose_name = "Palette"
        verbose_name_plural = "Palettes"
        ordering = ['-date_ajout']

    @property
    def nombre_produits_vendus(self):
        return self.products.aggregate(total=Sum('vendus'))['total'] or 0

    @property
    def benefice(self):
        total_vente = sum(product.price * product.vendus for product in self.products.all()) or 0
        return total_vente - self.prix_achat

    def save(self, *args, **kwargs):
        if not self.reference:
            super().save(*args, **kwargs)
            self.reference = f"PAL-{self.date_ajout.strftime('%y%m%d')}-{self.id:04d}"
            super().save(update_fields=['reference'])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.reference