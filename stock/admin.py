from stock.models import *

from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'quantity')
    list_filter = ['code']
    search_field = ['description', 'code']
    
admin.site.register(Product, ProductAdmin)
