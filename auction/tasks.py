from time import sleep
from celery import shared_task
from .models import Auction


@shared_task
def start_acution_task(auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if auction.status == 'pending':
        return
    auction.status = 'live'
    auction.save()
    print('-------AUCTION IS LIVE----------')
    print(auction.__dict__)


@shared_task
def close_acution_task(auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if auction.status == 'pending':
        return
    auction.status = 'closed'
    auction.save()
    print('-------AUCTION IS CLOSED----------')
    print(auction.__dict__)
    auction.update_products()
