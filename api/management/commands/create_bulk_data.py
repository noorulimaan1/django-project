from datetime import date, timedelta
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from accounts.models import User, Admin, Agent, Organization
from client.models import Lead, Customer

faker = Faker()


class Command(BaseCommand):
    help = 'Bulk create admins, agents, organizations, leads, and customers.'

    def get_unique_email(self, base_email, existing_emails):
        email = base_email
        counter = 1
        while email in existing_emails:
            email = f'{base_email.split(
                '@')[0]}_{counter}@{base_email.split('@')[1]}'
            counter += 1
        return email

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to generate data...'))

        organizations = []
        admins = []
        agents = []
        leads = []
        customers = []

        for _ in range(25):
            org_name = faker.unique.company()
            org_email = faker.unique.email()
            org_address = faker.address()
            org_phone = faker.phone_number()[:12]
            org_website = faker.unique.url()
            while Organization.objects.filter(name=org_name).exists():
                org_name = faker.unique.company()

            while Organization.objects.filter(email=org_email).exists():
                org_email = faker.unique.email()
            organization = Organization(
                name=org_name,
                email=org_email,
                address=org_address,
                phone_number=org_phone,
                website=org_website
            )
            organizations.append(organization)

        Organization.objects.bulk_create(organizations)

        organizations = Organization.objects.all()

        existing_user_emails = set(
            User.objects.values_list('email', flat=True))
        existing_lead_emails = set(
            Lead.objects.values_list('email', flat=True))

        for organization in organizations:
            admin_fname = faker.first_name()
            admin_lname = faker.last_name()
            admin_email = faker.unique.email()
            username = f'{admin_fname.lower()}.{admin_lname.lower()}_{
                random.randint(100, 999)}'
            password = make_password('joekim123')
            date_of_birth = faker.date_of_birth(minimum_age=25, maximum_age=50)

            admin_email = self.get_unique_email(
                admin_email, existing_user_emails)
            existing_user_emails.add(admin_email)

            admin_user = User(
                username=username,
                first_name=admin_fname,
                last_name=admin_lname,
                email=admin_email,
                password=password,
                date_of_birth=date_of_birth,
                role=1,
            )
            admin_user.save()
            admins.append(admin_user)

            if not Admin.objects.filter(org=organization).exists():
                Admin.objects.create(user=admin_user, org=organization)
            else:
                self.stdout.write(self.style.WARNING(
                    f'Admin already exists for organization: {organization.name}'))

        for organization in organizations:
            num_agents = random.randint(5, 15)
            for _ in range(num_agents):
                agent_fname = faker.first_name()
                agent_lname = faker.last_name()
                agent_email = faker.unique.email()
                username = f'{agent_fname.lower()}.{agent_lname.lower()}_{
                    random.randint(100, 999)}'
                password = make_password('joekim123')
                date_of_birth = faker.date_of_birth(
                    minimum_age=22, maximum_age=35)

                agent_email = self.get_unique_email(
                    agent_email, existing_user_emails)
                existing_user_emails.add(agent_email)

                agent_user = User(
                    username=username,
                    first_name=agent_fname,
                    last_name=agent_lname,
                    email=agent_email,
                    password=password,
                    date_of_birth=date_of_birth,
                    role=2,
                )
                agent_user.save()
                agents.append(agent_user)

                Agent.objects.create(user=agent_user, org=organization)

        agents = Agent.objects.all()

        for agent in agents:
            num_leads = random.randint(3, 5)
            for _ in range(num_leads):
                lead_email = faker.unique.email()
                lead_email = self.get_unique_email(
                    lead_email, existing_user_emails | existing_lead_emails)
                existing_lead_emails.add(lead_email)

                lead = Lead(
                    agent=agent,
                    organization=agent.org,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email=lead_email,
                    phone_number=faker.phone_number()[:12],
                    address=faker.address(),
                    category=random.choice([1, 2, 3])
                )
                leads.append(lead)

                if random.random() < 0.3:
                    customer_user = self.create_unique_user(lead)
                    if customer_user:
                        customer = Customer(
                            user=customer_user,
                            org=lead.organization,
                            lead=lead,
                            total_purchases=random.uniform(100, 10000),
                            first_purchase_date=faker.date_this_year(),
                            last_purchase_date=faker.date_this_year(),
                            agent=agent,
                        )
                        customers.append(customer)

        try:
            leads = self.remove_duplicate_leads(leads)
            Lead.objects.bulk_create(leads)
            Customer.objects.bulk_create(customers)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {
                              len(leads)} leads and {len(customers)} customers.'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(
                f'Error during bulk creation: {e}'))

    def create_unique_user(self, lead):
        try:
            base_username = faker.unique.user_name()
            random_suffix = random.randint(21, 78)
            username = f'{base_username}{random_suffix}'
            user = User.objects.create(
                username=username,
                first_name=lead.first_name,
                last_name=lead.last_name,
                email=lead.email,
                password=make_password('joekim123'),
                date_of_birth=faker.date_of_birth(
                    minimum_age=18, maximum_age=45),
                role=3
            )
            self.stdout.write(self.style.WARNING(
                f'CREATED! {username} created.'))
            return user
        except IntegrityError:
            self.stdout.write(self.style.WARNING(f'NOT CREATED! Email {
                              lead.email} or username already exists. Skipping user creation.'))
            return None

    def remove_duplicate_leads(self, leads):
        '''Remove any duplicate leads based on email from the list before bulk creation.'''
        unique_emails = set()
        unique_leads = []
        for lead in leads:
            if lead.email not in unique_emails:
                unique_emails.add(lead.email)
                unique_leads.append(lead)
        return unique_leads
