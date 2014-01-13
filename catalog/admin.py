from catalog.models import *
from django.contrib import admin

# Register your models here.

class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price_in', 'vat_in', 'gain_percentage', 'vat_out', 'price_out', 'lastchange_by', 'lastchange')
    list_filter = ['product']
    search_field = ['product']

admin.site.register(Price, PriceAdmin)

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_count')
    list_filter = ['title']
    search_field = ['title']

admin.site.register(Catalog, CatalogAdmin)
