from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Seller, Buyer
# Register your models here.


@admin.register(get_user_model())
class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Seller)
admin.site.register(Buyer)
