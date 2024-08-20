from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        # To make sure the database for this class is not created.
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # This links the custom manager (UserManager) to the User model.
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Admin(Timestamp):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="admin_profile")
    org = models.OneToOneField("Organization", on_delete=models.CASCADE, related_name="admin")
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    

    def __str__(self):
        return f"Admin: {self.user.email} - {self.org.name}"


class Organization(Timestamp):
    name = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Agent(Timestamp):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="agent_profile")
    org = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="agents"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hire_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=50, blank=True, null=True)


class Customer(Timestamp):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="customers"
    )
    lead = models.OneToOneField(
        "leads.Lead", on_delete=models.CASCADE, related_name="customer_lead"
    )
