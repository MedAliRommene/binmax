from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, DeliverySlip, ClientOrderHistory, EmployeeDeliveryHistory
from users.models import CustomUser

@receiver(post_save, sender=Order)
def create_delivery_slip_and_history(sender, instance, created, **kwargs):
    if created:
        # Créer un bon de livraison
        delivery_slip = DeliverySlip.objects.create(order=instance)
        # Ajouter à l'historique client
        ClientOrderHistory.objects.create(client=instance.client, order=instance)
        # Attribuer à un employé (premier disponible, ou logique à personnaliser)
        employee = CustomUser.objects.filter(role='EMPLOYE').first()
        if employee:
            delivery_slip.employee = employee
            delivery_slip.save()
            EmployeeDeliveryHistory.objects.create(employee=employee, delivery_slip=delivery_slip)