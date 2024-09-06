from django.contrib import admin

from client.models import Lead, Customer

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'age',)
    list_filter = ('first_name', )
    # search_fields = ('name',)# Column name in the list display

admin.site.register(Lead, PersonAdmin)
# admin.site.register(Lead)
admin.site.register(Customer)
