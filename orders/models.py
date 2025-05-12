from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from users.models import CustomUser, ClientProfile
from products.models import Product, ProductImage

class Cart(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts', limit_choices_to={'role': 'CLIENT'}, verbose_name="Client")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"
        ordering = ['-created_at']

    def __str__(self):
        return f"Panier de {self.client.username} ({self.created_at})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Panier")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produit")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Quantité")
    main_image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Image principale")

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ('cart', 'product')

    def save(self, *args, **kwargs):
        if not self.main_image:
            main_image = self.product.images.filter(is_main=True).first()
            self.main_image = main_image
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} dans panier {self.cart.id}"

class Order(models.Model):
    DELIVERY_TYPES = [
        ('DOMICILE', 'Livraison à domicile'),
        ('MAGASIN', 'Retrait en magasin'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PREPARING', 'En préparation'),
        ('SHIPPED', 'Expédié'),
        ('DELIVERED', 'Livré'),
    ]
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', limit_choices_to={'role': 'CLIENT'}, verbose_name="Client")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_TYPES, verbose_name="Type de livraison")
    delivery_address = models.TextField(verbose_name="Adresse de livraison")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Montant total")
    status = models.CharField(max_length=20, default='PENDING', choices=STATUS_CHOICES, verbose_name="Statut")

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.delivery_address and self.delivery_type == 'DOMICILE':
            self.delivery_address = self.client.client_profile.adresse
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} de {self.client.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Commande")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Produit")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Quantité")
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix à la commande")

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} dans commande {self.order.id}"

class DeliverySlip(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PREPARED', 'Préparé'),
        ('SHIPPED', 'Expédié'),
        ('DELIVERED', 'Livré'),  # Ajouté pour correspondre à Order.status
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_slip', verbose_name="Commande")
    employee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='delivery_slips', limit_choices_to={'role': 'EMPLOYE'}, verbose_name="Employé")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    status = models.CharField(max_length=20, default='PENDING', choices=STATUS_CHOICES, verbose_name="Statut")

    class Meta:
        verbose_name = "Bon de commande"
        verbose_name_plural = "Bons de commande"
        ordering = ['-created_at']

    def __str__(self):
        return f"Bon de commande pour  {self.order.id}"

class ClientOrderHistory(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order_history', limit_choices_to={'role': 'CLIENT'}, verbose_name="Client")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Commande")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        verbose_name = "Historique de commande client"
        verbose_name_plural = "Historiques de commandes clients"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande {self.order.id} pour {self.client.username}"

class EmployeeDeliveryHistory(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='delivery_history', limit_choices_to={'role': 'EMPLOYE'}, verbose_name="Employé")
    delivery_slip = models.ForeignKey(DeliverySlip, on_delete=models.CASCADE, verbose_name="Bon de commande")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        verbose_name = "Historique de livraison employé"
        verbose_name_plural = "Historiques de livraisons employés"
        ordering = ['-created_at']

    def __str__(self):
        return f"Livraison {self.delivery_slip.id} par {self.employee.username}"