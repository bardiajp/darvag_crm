# Generated by Django 5.1.7 on 2025-03-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_item_invoice_alter_item_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Product Price'),
        ),
    ]
