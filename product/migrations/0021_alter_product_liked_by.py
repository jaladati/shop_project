# Generated by Django 4.2.7 on 2024-03-22 15:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0020_product_liked_by_product_viewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_products', to=settings.AUTH_USER_MODEL, verbose_name='پسندیده شده توسط'),
        ),
    ]
