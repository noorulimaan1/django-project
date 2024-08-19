from django.db import models


# Create your models here.
class Lead(models.Model):
    agent = models.ForeignKey('accounts.Agent', on_delete=models.CASCADE, null=True, blank=True)  # Reference to Agent using a string
    org = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, null=True, blank=True)  # Reference to Organization using a string
    name = models.CharField(max_length=25)
    age = models.IntegerField() 
    description = models.TextField()
    email = models.EmailField()
    added_date = models.DateTimeField()
    category = models.TextField(default='unconverted')