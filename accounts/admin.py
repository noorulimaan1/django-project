from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User, Organization, Admin, Agent
from accounts.constants import ROLE_CHOICES, ADMIN

# Register your models here.

admin.site.register(Organization)
admin.site.register(Admin)
admin.site.register(Agent)


class AdminInline(admin.StackedInline):
    model = Admin
    can_delete = False
    verbose_name_plural = 'Admin Profile'
    fk_name = 'user'  


class CustomAdminCreationForm(UserCreationForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        help_text='Select an organization or create a new one.',
    )

    # role = forms.ChoiceField(
    #     choices=ROLE_CHOICES,
    #     required=True,
    #     help_text='Select a role for the user.',
    # )


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'organization', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = ADMIN
        org = self.cleaned_data.get('organization')

        if not org:
            org = Organization.objects.create(name='Default Organization')

        if commit:
            user.save()
            Admin.objects.create(user=user, org=org)

        return user


# Customizes how the User model is displayed and managed in the admin interface.
class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomAdminCreationForm 
    inlines = (AdminInline,)

    fieldsets = (
        (
            'Credentials', 
            {'fields': ('username', 'password')}
        ),
        (
            'Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'age', 'role')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'groups',
                    'user_permissions',
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',), 
                'fields': (
                    'first_name',
                    'last_name',
                    'username',
                    'email',
                    'age',
                    'password1',
                    'password2',
                    'profile_photo',
                    'date_of_birth',
                    'address',
                    'phone_number',
                    # 'role',
                    'organization',
                ),
            },
        ),
    )

    list_display = ('username',  'first_name', 'last_name', 'email', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'role')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
