from stock.models import *

from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'quantity')
    list_filter = ['code']
    search_field = ['name', 'code']
    
admin.site.register(Product, ProductAdmin)
