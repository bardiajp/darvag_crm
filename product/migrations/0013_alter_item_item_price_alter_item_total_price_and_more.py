# Generated by Django 5.1.7 on 2025-03-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_item_item_price_alter_item_quote_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Item Price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Total Price'),
        ),
        migrations.AlterField(
            model_name='pricebook',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Price Book Discount'),
        ),
        migrations.AlterField(
            model_name='pricebook',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Price Book'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Product Tax'),
        ),
    ]
