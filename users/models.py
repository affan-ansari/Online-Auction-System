from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    TYPE_CHOICES = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller'),
        ('Admin', 'Admin'),
    )
    user_type = models.CharField(
        choices=TYPE_CHOICES, max_length=10, default='Buyer')
    email = models.EmailField(unique=True, blank=False)
    image = models.ImageField(
        upload_to='profile_images', default='profile_images/avatar.png')


class Seller(TimeStampedModel, models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)


class Buyer(TimeStampedModel, models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
