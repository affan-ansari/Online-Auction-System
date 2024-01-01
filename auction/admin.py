from django.contrib import admin

from .models import Auction, Bid, Product, ProductImage

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Product)
admin.site.register(ProductImage)
