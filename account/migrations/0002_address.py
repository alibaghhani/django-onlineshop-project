# Generated by Django 5.0.4 on 2024-04-17 00:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=30)),
                ('street', models.CharField(max_length=250)),
                ('alley', models.CharField(max_length=250)),
                ('house_number', models.CharField(max_length=4)),
                ('full_address', models.CharField(max_length=250)),
                ('costumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costumer_address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]