import json
from django.core.management.base import BaseCommand, CommandError

from accounts.models import Agent, Organization
from client.models import Lead
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = ' Gets all the leads from a JSON file and ingests it into the database'

    def add_arguments(self, parser):
        parser.add_argument('leads_data', type=str, help='The path to the JSON file containing leads data.')

    def handle(self, *args, **kwargs):
        leads_data_path = kwargs['leads_data']
        
        try:
            with open(leads_data_path, 'r') as file:
                data = json.load(file) 

            for lead_data in data:
                try:
                    agent = Agent.objects.get(id=lead_data.get('agent'))
                    organization = Organization.objects.get(id=lead_data.get('organization'))

                    lead, created = Lead.objects.update_or_create(
                        email=lead_data['email'],
                        defaults={
                            'first_name': lead_data.get('first_name', ''),
                            'last_name': lead_data.get('last_name', ''),
                            'age': lead_data.get('age', None),
                            'phone_number': lead_data.get('phone_number', ''),
                            'address': lead_data.get('address', ''),
                            'category': lead_data.get('category', 2),
                            'agent': agent,
                            'organization': organization  
                        }
                    )
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'{action} lead: {lead_data["email"]}')
                except ValidationError as e:
                    self.stdout.write(f'Validation error for lead {lead_data.get("email")}: {str(e)}')
                except KeyError as e:
                    self.stdout.write(f'Missing key {e} in lead data')

        except FileNotFoundError:
            raise CommandError(f'File not found: {leads_data_path}')
        except json.JSONDecodeError:
            raise CommandError(f'Error decoding JSON file: {leads_data_path}')
        except Exception as e:
            raise CommandError(f'An error occurred: {str(e)}')

#python manage.py data_ingestion data/leads_data.json
