# Generated by Django 5.1 on 2024-08-19 15:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customer_lead'),
        ('leads', '0002_lead_agent_lead_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.lead'),
        ),
    ]
