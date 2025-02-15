from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import EmailVerificationToken

class Command(BaseCommand):
    help = 'Creates verification tokens for existing users'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(emailverificationtoken__isnull=True)
        created = 0
        for user in users:
            EmailVerificationToken.objects.create(
                user=user,
                is_verified=user.is_active  # Assume active users are verified
            )
            created += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created} verification tokens')
        ) 