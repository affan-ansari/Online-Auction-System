# Generated by Django 5.0 on 2024-01-02 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('BYR', 'BUYER'), ('SLR', 'SELLER'), ('ADM', 'ADMIN')], default='BYR', max_length=3),
        ),
    ]
