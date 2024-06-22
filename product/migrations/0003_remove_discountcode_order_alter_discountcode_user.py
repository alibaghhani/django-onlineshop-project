# Generated by Django 5.0.4 on 2024-05-23 11:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_title_product_detail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discountcode',
            name='order',
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_discount_code', to=settings.AUTH_USER_MODEL),
        ),
    ]