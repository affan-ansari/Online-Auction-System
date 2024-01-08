from telnetlib import STATUS
from dirtyfields import DirtyFieldsMixin
from django.db import models, transaction
from django.db.models import Max
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
    is_approved = models.BooleanField(default=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    unsold_product_ids = models.CharField(max_length=500, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=10, default='pending')

    def start_auction(self):
        self.status = 'live'
        self.save()

    def close_auction(self):
        with transaction.atomic():
            self.status = 'closed'
            self.save()
            self.update_products()

    def update_products(self):
        sold_products = self.get_sold_products()
        unsold_products = self.get_unsold_products()
        self.assign_winning_bid(sold_products)

        self.unsold_product_ids = ",".join(
            map(str, unsold_products.values_list('id', flat=True)))
        unsold_products.update(auction=None)

    def get_sold_products(self):
        return self.product_set.filter(bid__isnull=False).distinct()

    def get_unsold_products(self):
        return self.product_set.filter(bid__isnull=True)

    def assign_winning_bid(self, sold_products):
        for product in sold_products:
            winning_bid = product.get_winning_bid()
            winning_bid.is_winning_bid = True
            winning_bid.save()

    def get_class_name(self):
        return self.__class__.__name__

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

    def get_winning_bid(self):
        highest_bid_amount = self.bid_set.aggregate(Max('amount'))[
            'amount__max']
        winning_bid = self.bid_set.filter(
            amount=highest_bid_amount).first()
        return winning_bid

    def get_class_name(self):
        return self.__class__.__name__

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

    class Meta:
        unique_together = ('buyer', 'product',)

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return str(self.buyer.user.email) + "'s bid"
