# Generated by Django 5.1 on 2024-09-21 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_create_admins_and_orgs'),
        ('client', '0002_alter_customer_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer_by_agent', to='accounts.agent'),
        ),
    ]
