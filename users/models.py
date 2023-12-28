from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Seller(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)


class Buyer(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
