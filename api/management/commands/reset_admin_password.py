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
            user = (
                User.objects.filter(username=user_input, is_staff=True).first()
                or User.objects.filter(email=user_input, is_staff=True).first()
            )

            if not user:
                raise User.DoesNotExist

            user.set_password(default_password)
            user.save()

            self.stdout.write(
                f'Successfully reset password for admin user: {user.username}'
            )

        except User.DoesNotExist:
            raise CommandError(f'The admin does not exist.')

        except Exception as e:
            raise CommandError(f'An error occurred: {str(e)}')
