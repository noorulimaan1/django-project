# Generated by Django 5.1 on 2024-09-27 08:11

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('phone_number', models.CharField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in the format 92-3XX-XXXXXXX', regex='^92-3\\d{2}-\\d{7}$')])),
                ('address', models.TextField(blank=True, max_length=100, null=True)),
                ('category', models.SmallIntegerField(choices=[(1, 'Unconverted'), (2, 'New'), (3, 'Contacted'), (4, 'Converted')], default=2)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads_by_agent', to='accounts.agent')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads_by_organization', to='accounts.organization')),
            ],
            options={
                'unique_together': {('email', 'organization')},
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('total_purchases', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('first_purchase_date', models.DateField(blank=True, null=True)),
                ('last_purchase_date', models.DateField(blank=True, null=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_by_agent', to='accounts.agent')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='accounts.organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_profile', to=settings.AUTH_USER_MODEL)),
                ('lead', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_lead', to='client.lead')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
