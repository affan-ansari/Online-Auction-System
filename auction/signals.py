from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auction


@receiver(post_save, sender=Auction)
def update_auction_status(sender, instance, **kwargs):
    if instance.is_approved and instance.status != 'inactive':
        if instance.is_dirty('is_approved') or instance.is_dirty('status'):
            instance.status = 'inactive'
            instance.save()
