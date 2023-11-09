# Generated by Django 4.2.7 on 2023-11-09 12:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='off',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MaxValueValidator(100.0), django.core.validators.MinValueValidator(0.0)], verbose_name='تخفیف'),
        ),
    ]
