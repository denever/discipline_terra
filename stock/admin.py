from stock.models import *

from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'quantity')
    list_filter = ['code']
    search_field = ['description', 'code', 'barcode']
    
admin.site.register(Product, ProductAdmin)

class PackageAdmin(admin.ModelAdmin):
    list_display = ('product', 'barcode', 'size')
    list_filter = ['product']
    search_field = ['product', 'barcode']

admin.site.register(Package, PackageAdmin)
