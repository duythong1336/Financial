# Generated by Django 4.0.4 on 2022-05-17 15:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomewallet',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
