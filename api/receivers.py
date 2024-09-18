from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

from accounts.models import User
from accounts.constants import CUSTOMER

from client.models import Lead, Customer
from client.constants import LEAD_CATEGORY_CONVERTED


@receiver(post_save, sender=Lead)
def create_customer_on_lead_conversion(sender, instance, created, **kwargs):
    if not created:  
        if instance.category == LEAD_CATEGORY_CONVERTED:
            if not Customer.objects.filter(lead=instance).exists():

                username = f'{instance.first_name.lower()}.{instance.last_name.lower()}_{get_random_string(3)}'
                password = get_random_string(10)

                user = User.objects.create(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    username=username,
                    email=instance.email,
                    password=make_password(password),
                    is_active=True,
                    role = CUSTOMER
                )

                Customer.objects.create(
                    user=user,
                    org=instance.organization,
                    lead=instance,
                    total_purchases=0.00,
                )
