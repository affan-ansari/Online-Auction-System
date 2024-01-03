# Generated by Django 5.0 on 2024-01-02 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_buyer',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_seller',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('BYR', 'Buyer'), ('SLR', 'Seller'), ('ADM', 'Admin')], default='BYR', max_length=3),
        ),
    ]