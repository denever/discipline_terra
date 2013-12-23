from django import forms
from django.forms import TextInput, NumberInput, Select
from django.utils.translation import ugettext as _
from localflavor.it.forms import ITSocialSecurityNumberField, ITVatNumberField

from invoices.models import Customer, Order, Item
from invoices.widgets import ITPhoneNumberField, AddressFormField

class CustomerForm(forms.ModelForm):
    tax_code = ITSocialSecurityNumberField(label=_('Tax code'), widget=TextInput(attrs={'class': 'form-control'}))
    vat_code = ITVatNumberField(label=_('Vat code'), widget=TextInput(attrs={'class': 'form-control'}))
    phone = ITPhoneNumberField(label=_('Phone'), widget=TextInput(attrs={'class': 'form-control'}))
    address = AddressFormField(label=_('Address'))

    class Meta:
        model = Customer
        exclude = ('lastupdate', 'lastupdate_by')

        widgets = {
            'surname': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            # 'phone': TextInput(),attrs={'class': 'form-control'}
            # 'tax_code': TextInput(attrs={'class': 'form-control'}),
            # 'vat_code': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        widgets = {
            'customer': Select(attrs={'class': 'form-control'}),
            }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('order',)

        widgets = {
            'price': Select(attrs={'class': 'form-control'}),
            'pieces': NumberInput(attrs={'class': 'form-control'}),
            }
