# Generated by Django 5.1.7 on 2025-03-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_alter_invoice_discount_alter_invoice_final_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Final price'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Total price'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='final_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Final price'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Tax'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=20, null=True, verbose_name='Total price'),
        ),
    ]
