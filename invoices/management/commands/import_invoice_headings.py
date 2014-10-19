from django.core.management.base import BaseCommand, CommandError

import sqlite3
from invoices.models import InvoiceHeading
from accounts.models import UserProfile


class Command(BaseCommand):
    """
    Create first user profile for existing user
    """
    help = 'Create first user profile for existing user'

    query = """select short_name,
                      long_name,
                      address,
                      tax_code,
                      phone,
                      email,
                      logo_filename,
                      lastchange_by_id,
                      lastchange from invoices_invoiceheading"""

    def handle(self, *args, **options):
        try:
            conn = sqlite3.connect(args[0])

            src_cur = conn.execute()
            for row in src_cur:
                obj = InvoiceHeading(short_name=row[0],
                                     long_name=row[1],
                                     address=row[2],
                                     tax_code=row[3],
                                     phone=row[4],
                                     email=row[5],
                                     logo_filename=row[6],
                                     lastchange_by=UserProfile.objects.get(id=row[7]),
                                     lastchange=row[8],
                                     usual_title_respect='Spett.le')
                obj.save()
        except Exception:
            raise CommandError
