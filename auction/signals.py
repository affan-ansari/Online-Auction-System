from datetime import datetime, timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Auction
from .tasks import start_acution_task, close_acution_task


@receiver(post_save, sender=Auction)
def update_auction_status(sender, instance: Auction, created, **kwargs):
    if created:
        start_acution_task.apply_async((instance.pk,), eta=instance.start_time)
        close_acution_task.apply_async((instance.pk,), eta=instance.end_time)
    if instance.is_approved and instance.status == 'pending':
        instance.status = 'inactive'
        instance.save()
