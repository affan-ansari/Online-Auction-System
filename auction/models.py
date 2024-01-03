from telnetlib import STATUS
from dirtyfields import DirtyFieldsMixin
from django.db import models
from users.models import Seller, Buyer
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Auction(DirtyFieldsMixin, TimeStampedModel, TitleDescriptionModel, models.Model):
    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('inactive', 'INACTIVE'),
        ('live', 'LIVE'),
        ('closed', 'CLOSED'),
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    minimum_bids = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    unsold_product_ids = models.CharField(max_length=500, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=10, default='pending')

    def __str__(self):
        return self.title


class Product(DirtyFieldsMixin, TimeStampedModel, TitleDescriptionModel, models.Model):
    STATUS_CHOICES = (
        ('sold', 'SOLD'),
        ('live', 'LIVE'),
        ('inactive', 'INACTIVE'),
    )

    minimum_bid = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15)

    def __str__(self):
        return self.title


class ProductImage(TimeStampedModel, models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='product_images', default='product_images/product_avatar.png')


class Bid(DirtyFieldsMixin, TimeStampedModel, models.Model):
    amount = models.IntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_winning_bid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.buyer.user.email) + "'s bid"
