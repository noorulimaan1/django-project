from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from client.constants import (
    LEAD_CATEGORIES,
    LEAD_CATEGORY_UNCONVERTED,
    LEAD_CATEGORY_CONTACTED,
    LEAD_CATEGORY_CONVERTED,
    LEAD_CATEGORY_NEW,
)

from accounts.models import Timestamp, Organization


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
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    age = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)

    category = models.SmallIntegerField(
        choices=[(key, value) for key, value in LEAD_CATEGORIES.items()],
        default=LEAD_CATEGORY_NEW,
    )

    def clean(self):
        super().clean()

        if self.pk:  # if it's an existing lead
            previous_lead = Lead.objects.get(pk=self.pk)

            # Only check category if it is being changed
            if self.category != previous_lead.category:
                if previous_lead.category == LEAD_CATEGORY_NEW:
                    if self.category not in [
                        LEAD_CATEGORY_CONTACTED,
                        LEAD_CATEGORY_UNCONVERTED,
                    ]:
                        raise ValidationError(
                            'Lead status must transition from New to Contacted or Unconverted.'
                        )

                elif previous_lead.category == LEAD_CATEGORY_CONTACTED:
                    if self.category not in [
                        LEAD_CATEGORY_CONVERTED,
                        LEAD_CATEGORY_UNCONVERTED,
                    ]:
                        raise ValidationError(
                            'Lead status must transition from Contacted to Converted or Unconverted.'
                        )

                elif previous_lead.category == LEAD_CATEGORY_CONVERTED:
                    raise ValidationError(
                        'Lead status cannot be changed once it is Converted.'
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name}'


class Customer(Timestamp):
    user = models.OneToOneField(
        'accounts.User', on_delete=models.CASCADE, related_name='customer_profile'
    )
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='customers'
    )
    lead = models.OneToOneField(
        'client.Lead', on_delete=models.CASCADE, related_name='customer_lead', blank=True, null=True
    )
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    first_purchase_date = models.DateField(null=True, blank=True)
    last_purchase_date = models.DateField(null=True, blank=True)
    agent = models.ForeignKey(
        'accounts.Agent', on_delete=models.CASCADE, related_name='customer_by_agent', blank=True, null=True
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
