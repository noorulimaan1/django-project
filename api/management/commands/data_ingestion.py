from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
import json

from api.utilities import ingest_leads


from accounts.models import Agent, Organization
from client.models import Lead


class Command(BaseCommand):
    help = ' Gets all the leads from a JSON file and ingests it into the database'

    def add_arguments(self, parser):
        parser.add_argument('leads_data', type=str, help='The path to the JSON file containing leads data.')

    def handle(self, *args, **kwargs):
        leads_data_path = kwargs['leads_data']
        
        try:
            with open(leads_data_path, 'r') as file:
                data = json.load(file) 

            results = ingest_leads(data)

            for result in results:
                if 'error' in result:
                    self.stdout.write(f"Error for {result['email']}: {result['error']}")
                else:
                    self.stdout.write(f"{result['action']} lead: {result['email']}")
             
        except FileNotFoundError:
            raise CommandError(f'File not found: {leads_data_path}')
        except json.JSONDecodeError:
            raise CommandError(f'Error decoding JSON file: {leads_data_path}')
        except Exception as e:
            raise CommandError(f'An error occurred: {str(e)}')
