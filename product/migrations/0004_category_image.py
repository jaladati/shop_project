# Generated by Django 4.2.7 on 2023-11-16 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_image_productgallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='imaegs/categories', verbose_name='تصویر'),
        ),
    ]