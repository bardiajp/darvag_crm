# Generated by Django 5.1.7 on 2025-03-09 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('birth_date', models.DateField(verbose_name='Birth Date')),
                ('mobile_number', models.CharField(max_length=11, verbose_name='Mobile Number')),
                ('phone_number', models.CharField(max_length=11, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('state', models.CharField(max_length=25, verbose_name='State')),
                ('zip_code', models.CharField(max_length=10, verbose_name='Zip Code')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('company_no', models.CharField(max_length=50, verbose_name='Company No')),
                ('industry', models.CharField(max_length=50, verbose_name='Industry')),
                ('register_code', models.IntegerField(verbose_name='Register Code')),
                ('mobile_number', models.CharField(max_length=15, verbose_name='Mobile Number')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('city', models.CharField(max_length=50, verbose_name='City')),
                ('state', models.CharField(max_length=25, verbose_name='State')),
                ('zip_code', models.CharField(max_length=10, verbose_name='Zip Code')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='accounts.user')),
                ('user', models.ManyToManyField(related_name='company_users', to='accounts.user')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'db_table': 'companies',
            },
        ),
    ]
