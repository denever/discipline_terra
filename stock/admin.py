from django.contrib import admin

from .models import Category, Package, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "quantity", "lastchange_by", "lastchange")
    list_filter = ["category"]
    search_field = ["description", "code", "barcode"]


admin.site.register(Product, ProductAdmin)


class PackageAdmin(admin.ModelAdmin):
    list_display = ("product", "barcode", "size", "lastchange_by", "lastchange")
    list_filter = ["product"]
    search_field = ["product", "barcode"]


admin.site.register(Package, PackageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ["name"]
    search_field = ["name", "description"]


admin.site.register(Category, CategoryAdmin)
