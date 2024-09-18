from celery import shared_task
from django.core.management import call_command


@shared_task(name='ingest_lead_data')
def ingest_leads():
    print('Starting lead ingestion task')
    call_command('data_ingestion', 'data/leads_data.json')
