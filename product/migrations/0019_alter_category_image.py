# Generated by Django 4.2.7 on 2024-02-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_productcolorvariant_off_productcolorvariant_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='images/categories', verbose_name='تصویر'),
        ),
    ]