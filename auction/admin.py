from django.contrib import admin

from .models import Auction, Bid, Product

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Product)
