# Generated by Django 5.0 on 2024-01-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_is_admin_remove_user_is_buyer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('Buyer', 'Buyer'), ('Seller', 'Seller'), ('Admin', 'Admin')], default='BYR', max_length=10),
        ),
    ]
