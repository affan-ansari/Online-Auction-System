# Generated by Django 5.0 on 2023-12-31 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_auction_is_approved_auction_minimum_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]