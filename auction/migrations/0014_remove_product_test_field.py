# Generated by Django 5.0 on 2024-01-12 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_product_test_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='test_field',
        ),
    ]
