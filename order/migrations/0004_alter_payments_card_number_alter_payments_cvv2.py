# Generated by Django 5.0.4 on 2024-06-10 13:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='card_number',
            field=models.IntegerField(max_length=16),
        ),
        migrations.AlterField(
            model_name='payments',
            name='cvv2',
            field=models.IntegerField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\d{3,4}$')]),
        ),
    ]
