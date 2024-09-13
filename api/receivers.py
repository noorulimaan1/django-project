from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from client.models import Lead, Customer
from accounts.models import User  # Assuming the User model is in a separate app
from client.constants import LEAD_CATEGORY_CONVERTED  # Ensure this is imported correctly

@receiver(post_save, sender=Lead)
def create_customer_on_lead_conversion(sender, instance, created, **kwargs):
    # This will run whenever a lead is saved
    if not created:  # Only act on updates, not creation
        if instance.category == LEAD_CATEGORY_CONVERTED:
            # Check if Customer already exists
            if not Customer.objects.filter(lead=instance).exists():
                
                # Create user based on the lead's details
                username = f"{instance.first_name.lower()}.{instance.last_name.lower()}_{get_random_string(3)}"
                password = get_random_string(10)

                user = User.objects.create(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    username=username,
                    email=instance.email,
                    password=make_password(password),
                    is_active=True,
                )

                # Create the customer linked to the lead
                Customer.objects.create(
                    user=user,
                    org=instance.organization,
                    lead=instance,
                    total_purchases=0.00,
                )
