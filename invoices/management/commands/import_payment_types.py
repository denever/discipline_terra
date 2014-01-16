from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

import sqlite3
from invoices.models import Payment

class Command(BaseCommand):
    """
    Create first user profile for existing user
    """
    help = 'Create first user profile for existing user'

    def handle(self, *args, **options):
        conn = sqlite3.connect(args[0])

        src_cur = conn.execute('select name from invoices_payment;')
        for row in src_cur:
            obj = Payment(name=row[0])
            obj.save()
