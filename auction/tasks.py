from time import sleep
from celery import shared_task
from .models import Auction


@shared_task
def start_acution_task(auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if auction.status in ['pending', 'closed', 'live']:
        return
    auction.start_auction()
    print('-------AUCTION IS LIVE----------')
    print(auction.__dict__)


@shared_task
def close_acution_task(auction_pk):
    auction = Auction.objects.get(pk=auction_pk)
    if auction.status in ['pending', 'closed']:
        return
    auction.close_auction()
    print('-------AUCTION IS CLOSED----------')
    print(auction.__dict__)
