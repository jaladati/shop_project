# Generated by Django 4.2.7 on 2023-12-15 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_remove_product_color_variant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcolorvariant',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_variants', to='product.product', verbose_name='محصول'),
        ),
    ]
