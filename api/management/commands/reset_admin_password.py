from django.core.management.base import BaseCommand, CommandError

from accounts.models import User, Admin


class Command(BaseCommand):
    help = 'Reset password for an admin user to a default value'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='The username or email of the admin whose password will be reset.',
        )

    def handle(self, *args, **kwargs):
        user_input = kwargs['user']
        default_password = 'default123'

        if not user_input:
            self.stdout.write(self.style.ERROR('The --user argument is required.'))
            return

        try:
            # Try to get the user by username first, fallback to email if not found
            try:
                user = User.objects.get(username=user_input)
            except User.DoesNotExist:
                user = User.objects.get(email=user_input)

            # Ensure the user is an admin
            if user.role != 1:
                raise CommandError('The user is not an admin.')

            # Set the new password and save the user
            user.set_password(default_password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'Successfully reset password for admin user: {user.username}')
            )

        except User.DoesNotExist:
            raise CommandError('The admin does not exist.')
        except Exception as e:
            raise CommandError(f'An error occurred: {str(e)}')
