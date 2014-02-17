from invoices.models import *
from django.contrib import admin

# Register your models here.

from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'record_date', 'invoiced', 'lastchange_by', 'lastchange')
    list_filter = ['customer']
    search_field = ['customer', 'barcode']

admin.site.register(Order, OrderAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'voice_count', 'amount', 'issuer')
    list_filter = ['customer']
    search_field = ['customer', 'barcode']

admin.site.register(Invoice, InvoiceAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount_novat', 'amount')
    list_filter = []
    search_field = ['name']

admin.site.register(Payment, PaymentAdmin)

class InvoiceHeadingAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name', 'tax_code')
    list_filter = []
    search_field = ['short_name']

admin.site.register(InvoiceHeading, InvoiceHeadingAdmin)
