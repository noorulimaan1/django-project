from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from accounts.models import User, Organization, Admin, Agent


# Register your models here.
# admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Admin)
admin.site.register(Agent)





class AdminInline(admin.StackedInline):
    model = Admin
    can_delete = False
    verbose_name_plural = 'Admin Profile'
    fk_name = 'user'


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        help_text='Select an organization or create a new one.',
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True

        org = self.cleaned_data.get('organization')
        if not org:
            org = Organization.objects.create(name='Default Organization')

        if commit:
            user.save()
            Admin.objects.create(user=user, org=org)

        return user


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = (AdminInline,)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Personal info',
            {'fields': ('first_name', 'last_name', 'email', 'age', 'profile_photo')},
        ),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            },
        ),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'organization',
                ),
            },
        ),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
