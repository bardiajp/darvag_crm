# Generated by Django 5.1.7 on 2025-03-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='period',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
