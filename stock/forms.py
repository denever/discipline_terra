from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext as _

from stock.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('lastupdate', 'lastupdate_by')

        widgets = {
            'code': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'quantity': TextInput(attrs={'class': 'form-control'}),
            'producer': TextInput(attrs={'class': 'form-control'}),
        }
