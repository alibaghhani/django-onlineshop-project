# Generated by Django 5.0.4 on 2024-04-19 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_category_sub_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='type_of_discount',
            field=models.CharField(blank=True, choices=[('percentage', '%'), ('cash', '$')], max_length=250, null=True),
        ),
    ]