# Generated by Django 4.2.7 on 2024-08-25 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'تیکت', 'verbose_name_plural': 'تیکت ها'},
        ),
        migrations.AlterField(
            model_name='ticket',
            name='subject',
            field=models.CharField(choices=[('PR', 'پیشنهاد'), ('CR', 'انتقاد'), ('RP', 'گزارش')], max_length=2, verbose_name='موضوع'),
        ),
    ]
