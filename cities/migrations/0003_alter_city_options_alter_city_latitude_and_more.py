# Generated by Django 4.0.2 on 2022-02-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_alter_city_latitude_alter_city_longitude_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterField(
            model_name='city',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True),
        ),
    ]
