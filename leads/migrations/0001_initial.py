# Generated by Django 5.1 on 2024-08-20 12:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(choices=[('Unconverted', 'Unconverted'), ('New', 'New'), ('Contacted', 'Contacted'), ('Converted', 'Converted')], default='Unconverted', max_length=11)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads_by_agent', to='accounts.agent')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads_by_organization', to='accounts.organization')),
            ],
        ),
    ]
