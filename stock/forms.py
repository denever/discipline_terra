from django import forms
from django.contrib.admin import widgets
from django.utils.translation import ugettext as _

from stock.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('lastupdate', 'lastupdate_by')
