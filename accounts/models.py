from datetime import date
from django.core.validators import MinValueValidator, RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from accounts.constants import (
    ROLE_CHOICES,
    AGENT,

)

# Create your models here.


class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True, blank=True,
                              null=True, max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    profile_photo = models.ImageField(
        upload_to=upload_to, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True, max_length=200)
    phone_number = models.CharField(validators=[
        RegexValidator(
            regex=r'^92-3\d{2}-\d{7}$',
            message='Phone number must be in the format 92-3XX-XXXXXXX'
        )
    ], blank=True, null=True)

    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=AGENT)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None


class Admin(Timestamp):
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, related_name='admin_profile'
    )
    org = models.OneToOneField(
        'Organization', on_delete=models.CASCADE, related_name='admin'
    )

    def __str__(self):
        return f'Admin: {self.user.username} - {self.org.name}'


class Organization(Timestamp):
    name = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=50)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(validators=[
        RegexValidator(
            regex=r'^92-3\d{2}-\d{7}$',
            message='Phone number must be in the format 92-3XX-XXXXXXX'
        )
    ], blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Agent(Timestamp):
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, related_name='agent_profile'
    )
    org = models.ForeignKey(
        'Organization', on_delete=models.CASCADE, related_name='agents'
    )
    hire_date = models.DateField(null=True, blank=True)

    def form_valid(self, form):
        form.instance.org = self.request.user.admin_profile.org
        return super().form_valid(form)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
