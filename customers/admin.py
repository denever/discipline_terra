from django.contrib import admin

from customers.models import Customer


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "address", "lastchange_by", "lastchange")
    list_filter = ["surname"]
    search_field = ["name", "surname"]


admin.site.register(Customer, CustomerAdmin)
