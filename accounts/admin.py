from django.contrib import admin
from .models import User, Organization, Admin, Agent, Customer

# Register your models here.
admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Admin)
admin.site.register(Agent)
admin.site.register(Customer)
