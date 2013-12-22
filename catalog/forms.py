from django.forms import ModelForm, TextInput, NumberInput, Select
from django.utils.translation import ugettext as _

from catalog.models import Price

class PriceForm(ModelForm):
    class Meta:
        model = Price
        exclude = ('lastupdate', 'lastupdate_by')

        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'price_in': NumberInput(attrs={'class': 'form-control'}),
            'vat_in': NumberInput(attrs={'class': 'form-control'}),
            'vat_out': NumberInput(attrs={'class': 'form-control'}),
            'gain_percentage': NumberInput(attrs={'class': 'form-control'}),            
        }
