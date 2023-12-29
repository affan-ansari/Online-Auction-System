from django.db import models
from users.models import Seller, Buyer
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Auction(TimeStampedModel, TitleDescriptionModel, models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    unsold_product_ids = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.seller.user.email) + "'s auction"


class Product(TimeStampedModel, TitleDescriptionModel, models.Model):
    minimum_bid = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, null=True, blank=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Bid(TimeStampedModel, models.Model):
    amount = models.IntegerField
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_winning_bid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.buyer.user.email) + "'s bid"
