from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seller, User, Buyer


@receiver(post_save, sender=User)
def create_user(sender, instance: User, created, **kwargs):
    if instance.user_type == 'Buyer':
        Buyer.objects.get_or_create(user=instance)
    elif instance.user_type == 'Seller':
        Seller.objects.get_or_create(user=instance)
