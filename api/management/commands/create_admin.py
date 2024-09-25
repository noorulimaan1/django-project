import random
from django.core.management.base import BaseCommand
from accounts.models import Organization, User, Admin
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create admins and their organizations.'

    def add_arguments(self, parser):
        # Organization-related arguments (some are required)
        parser.add_argument('--org_name', type=str, required=True, help='Name of the organization')
        parser.add_argument('--org_email', type=str, required=True, help='Email for the organization')
        parser.add_argument('--org_website', type=str, default='https://defaultorg.com', help='Website for the organization')
        parser.add_argument('--org_address', type=str, default='123 Default Street', help='Address for the organization')
        parser.add_argument('--org_phone', type=str, default='123-456-7890', help='Phone number for the organization')

        # Admin-related arguments (some are required)
        parser.add_argument('--admin_fname', type=str, required=True, help="Admin's first name")
        parser.add_argument('--admin_lname', type=str, required=True, help="Admin's last name")
        parser.add_argument('--admin_email', type=str, required=True, help="Admin's email address")
        parser.add_argument('--admin_age', type=int, help="Admin's age")
        parser.add_argument('--admin_address', type=str, default='', help="Admin's address")
        parser.add_argument('--admin_phone', type=str, default='', help="Admin's phone number")
        parser.add_argument('--admin_dob', type=str, help="Admin's date of birth (YYYY-MM-DD)")

    def handle(self, *args, **kwargs):
        # Organization data
        org_name = kwargs['org_name']
        org_email = kwargs['org_email']
        org_website = kwargs.get('org_website')
        org_address = kwargs.get('org_address')
        org_phone = kwargs.get('org_phone')

        # Admin data
        admin_fname = kwargs['admin_fname']
        admin_lname = kwargs['admin_lname']
        admin_email = kwargs['admin_email']
        admin_age = kwargs.get('admin_age')
        admin_address = kwargs.get('admin_address', '')
        admin_phone = kwargs.get('admin_phone', '')
        admin_dob = kwargs.get('admin_dob', None)

        # Create organization
        org = Organization.objects.create(
            name=org_name,
            email=org_email,
            address=org_address,
            phone_number=org_phone,
            website=org_website
        )

        # Generate admin username and password
        username = f'{admin_fname.lower()}.{admin_lname.lower()}_{random.randint(100, 999)}'
        password = get_random_string(10)

        # Create admin user
        admin_user = User.objects.create(
            username=username,
            first_name=admin_fname,
            last_name=admin_lname,
            email=admin_email,
            age=admin_age,
            address=admin_address,
            phone_number=admin_phone,
            date_of_birth=admin_dob,
            password=make_password(password),  # Hash the password
            role=1,  # Assuming '1' is the role for admins

        )

        # Create Admin profile associated with the organization
        Admin.objects.create(user=admin_user, org=org)

        # Output generated username and password to the console
        self.stdout.write(self.style.SUCCESS(f"Successfully created admin '{admin_user.username}' with password '{password}' for organization '{org_name}'"))
