from django.forms import ModelForm, TextInput, NumberInput, Select
from django.utils.translation import ugettext as _

from stock.models import Product, Package

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('lastupdate', 'lastupdate_by')

        widgets = {
            'code': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'wrn_tsh': NumberInput(attrs={'class': 'form-control'}),
            'producer': TextInput(attrs={'class': 'form-control'}),
            'barcode': NumberInput(attrs={'class': 'form-control'}),            
        }

class PackageForm(ModelForm):
    class Meta:
        model = Package
        exclude = ('lastupdate', 'lastupdate_by')
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),            
            'size': NumberInput(attrs={'class': 'form-control'}),
            'barcode': NumberInput(attrs={'class': 'form-control'}),
        }
