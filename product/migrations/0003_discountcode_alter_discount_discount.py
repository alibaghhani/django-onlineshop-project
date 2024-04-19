# Generated by Django 5.0.4 on 2024-04-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_category_expired_at_remove_product_expired_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=8, null=True, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.PositiveIntegerField(blank=True, max_length=250, null=True, unique=True),
        ),
    ]
