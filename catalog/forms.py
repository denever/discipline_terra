from django.forms import ModelForm, TextInput, NumberInput, Select
from django.utils.translation import ugettext as _

from catalog.models import Price, Catalog

class CatalogForm(ModelForm):
    class Meta:
        model = Catalog
        exclude = ('lastchange', 'lastchange_by')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
        }

class PriceForm(ModelForm):
    class Meta:
        model = Price
        exclude = ('lastchange', 'lastchange_by')

        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'catalog': Select(attrs={'class': 'form-control'}),
            'price_in': NumberInput(attrs={'class': 'form-control'}),
            'vat_in': NumberInput(attrs={'class': 'form-control'}),
            'vat_out': NumberInput(attrs={'class': 'form-control'}),
            'gain_percentage': NumberInput(attrs={'class': 'form-control'}),
        }
