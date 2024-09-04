from django.db import models
from django.core.validators import MinValueValidator

from client.constants import LEAD_CATEGORIES, LEAD_CATEGORY_NEW

from accounts.models import Timestamp, User, Organization


# Create your models here.
class Lead(Timestamp):

    agent = models.ForeignKey(
        'accounts.Agent', on_delete=models.CASCADE, related_name='leads_by_agent'
    )
    organization = models.ForeignKey(
        'accounts.Organization',
        on_delete=models.CASCADE,
        related_name='leads_by_organization',
    )
    name = models.CharField(max_length=25)
    age = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)

    category = models.SmallIntegerField(
        choices=[(key, value) for key, value in LEAD_CATEGORIES.items()],
        default=LEAD_CATEGORY_NEW,
    )

    def __str__(self):
        return f'{self.name}'


class Customer(Timestamp):
    user = models.OneToOneField(
        'accounts.User', on_delete=models.CASCADE, related_name='customer_profile'
    )
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='customers'
    )
    lead = models.OneToOneField(
        'client.Lead', on_delete=models.CASCADE, related_name='customer_lead'
    )
    total_purchases = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    first_purchase_date = models.DateField(null=True, blank=True)
    last_purchase_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Customer: {self.lead.first_name} {self.lead.last_name} - Total Purchases: {self.total_purchases}'
