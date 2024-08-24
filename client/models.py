from django.db import models
from django.core.validators import MinValueValidator
from .constants import LEAD_CATEGORIES, LEAD_CATEGORY_UNCONVERTED



# Create your models here.
class Lead(models.Model):
    # user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, related_name="lead_profile")
    agent = models.ForeignKey("accounts.Agent", on_delete=models.CASCADE, related_name="leads_by_agent")
    organization = models.ForeignKey("accounts.Organization", on_delete=models.CASCADE, related_name="leads_by_organization")
    name = models.CharField(max_length=25)
    age = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(max_length=100, blank=True, null=True)

    category = models.CharField(
        max_length=11, choices=LEAD_CATEGORIES.items(), default=LEAD_CATEGORY_UNCONVERTED
    )

    def __str__(self):
        return f"{self.name}"



