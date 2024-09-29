from django.contrib import admin

from client.models import Lead, Customer

# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',

    )
    list_filter = ('first_name',)


admin.site.register(Lead, PersonAdmin)
admin.site.register(Customer)
