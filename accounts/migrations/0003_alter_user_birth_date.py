# Generated by Django 5.1.7 on 2025-03-09 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_managers_remove_user_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(default='2000-01-01', verbose_name='Birth Date'),
        ),
    ]
