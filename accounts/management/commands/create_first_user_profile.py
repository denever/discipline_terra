from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

# importing User for UserProfile
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    """
    Create first user profile for existing user
    """
    help = 'Create first user profile for existing user'

    def handle(self, *args, **options):
        u = User.objects.get(id=1)
        up = UserProfile(user=u)
        up.save()
