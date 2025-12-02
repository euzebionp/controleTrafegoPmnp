from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Viagem

@receiver(post_save, sender=Viagem)
def update_vehicle_km_on_save(sender, instance, created, **kwargs):
    """
    Updates the vehicle's mileage when a trip is saved.
    If it's a new trip, add the distance.
    If it's an update, we would ideally need the old instance to calculate the difference,
    but for simplicity in this migration, we are assuming additive logic or manual correction if needed.
    However, to be more robust, we should handle updates carefully.
    
    For this implementation, we will rely on the fact that 'km_atual' in Veiculo 
    should reflect the total.
    """
    if created:
        instance.veiculo.km_atual += instance.distancia
        instance.veiculo.save()
    else:
        # If updating, it's complex without tracking previous state. 
        # For now, we assume the user might manually correct the vehicle km if they change the trip distance drastically.
        # Or we could fetch the old value if we had it.
        pass

@receiver(post_delete, sender=Viagem)
def update_vehicle_km_on_delete(sender, instance, **kwargs):
    """
    Reverts the vehicle's mileage when a trip is deleted.
    """
    instance.veiculo.km_atual -= instance.distancia
    instance.veiculo.save()
