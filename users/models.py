from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_seller = models.BooleanField(default=False, blank=False)
    is_buyer = models.BooleanField(default=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    image = models.ImageField(
        upload_to='profile_images', default='profile_images/avatar.png')


class Seller(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)


class Buyer(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
