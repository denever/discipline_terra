from django.forms import ModelForm, TextInput, NumberInput, Select
from stock.models import Product, Package, Category


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('lastchange', 'lastchange_by')

        widgets = {
            'code': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'quantity': NumberInput(attrs={'class': 'form-control'}),
            'wrn_tsh': NumberInput(attrs={'class': 'form-control'}),
            'producer': TextInput(attrs={'class': 'form-control'}),
            'barcode': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
        }


class PackageForm(ModelForm):
    class Meta:
        model = Package
        exclude = ('lastchange', 'lastchange_by')
        widgets = {
            'product': Select(attrs={'class': 'form-control'}),
            'size': NumberInput(attrs={'class': 'form-control'}),
            'barcode': NumberInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('lastchange', 'lastchange_by')
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
        }
