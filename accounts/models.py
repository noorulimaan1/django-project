from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    #username, first_name, last_name, email, password
    pass


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Organization(models.Model):
    name = models.CharField(max_length=50)
    admin = models.OneToOneField(Admin, on_delete=models.CASCADE)

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey('Organization', on_delete=models.CASCADE)
    

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    conversion_date = models.DateTimeField()
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
