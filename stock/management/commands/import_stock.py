from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

import sqlite3
# importing User for UserProfile
from django.contrib.auth.models import User
from stock.models import *
from accounts.models import UserProfile

class Command(BaseCommand):
    """
    Create first user profile for existing user
    """
    help = 'Create first user profile for existing user'

    def handle(self, *args, **options):
        author = UserProfile.objects.get(id=1)
        conn = sqlite3.connect(args[0])
#        conn.row_factory = sqlite3.Row
        src_cur = conn.execute('select code, description, producer, barcode from stock_product;')
        for row in src_cur:
            obj = Product(code=row[0], description=row[1], producer=row[2], barcode=row[3], quantity=0, wrn_tsh=1, lastupdate_by=author)
            obj.save()

        src_cur = conn.execute('select product_id, size, barcode from stock_package')
        for row in src_cur:
            obj = Package(product_id=row[0], size=row[1], barcode=row[2], lastupdate_by=author)
            obj.save()
