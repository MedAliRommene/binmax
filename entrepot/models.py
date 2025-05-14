from django.db import models

class Entrepot(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")
    adresse = models.TextField(blank=True, verbose_name="Adresse")

    class Meta:
        verbose_name = "Entrepôt"
        verbose_name_plural = "Entrepôts"
        ordering = ['code']

    def __str__(self):
        return f"ENT-{self.code}"

class Zone(models.Model):
    entrepot = models.ForeignKey(Entrepot, on_delete=models.PROTECT, related_name='zones', verbose_name="Entrepôt")
    code = models.CharField(max_length=10, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")

    class Meta:
        unique_together = ('entrepot', 'code')
        verbose_name = "Zone"
        verbose_name_plural = "Zones"
        ordering = ['entrepot__code', 'code']

    def __str__(self):
        return f"{self.entrepot.code}-ZONE-{self.code}"

class Rayon(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name='rayons', verbose_name="Zone")
    code = models.CharField(max_length=10, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Nom")
    emplacement_limit = models.PositiveIntegerField(default=0, verbose_name="Limite d'emplacements")
    emplacement_used = models.PositiveIntegerField(default=0, verbose_name="Emplacements utilisés", editable=False)

    class Meta:
        unique_together = ('zone', 'code')
        verbose_name = "Rayon"
        verbose_name_plural = "Rayons"
        ordering = ['zone__entrepot__code', 'zone__code', 'code']

    @property
    def emplacement_available(self):
        return self.emplacement_limit - self.emplacement_used

    def __str__(self):
        return f"{self.zone.entrepot.code}-{self.zone.code}-RAYON-{self.code}"