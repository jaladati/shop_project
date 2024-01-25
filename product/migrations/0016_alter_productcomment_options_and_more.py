# Generated by Django 4.2.7 on 2024-01-19 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_alter_productspecification_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcomment',
            options={'verbose_name': 'نظر', 'verbose_name_plural': 'نظرات'},
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='product.productcomment', verbose_name='والد'),
        ),
    ]