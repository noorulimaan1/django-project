from accounts.models import Agent, Organization
from client.models import Lead
from django.core.exceptions import ValidationError

def ingest_leads(data):
    results = []
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
            results.append({'email': lead_data['email'], 'action': action})
        
        except ValidationError as e:
            results.append({'email': lead_data.get('email'), 'error': str(e)})
        except KeyError as e:
            results.append({'email': lead_data.get('email'), 'error': f'Missing key {e}'})
    
    return results
