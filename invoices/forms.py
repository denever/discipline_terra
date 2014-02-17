from django import forms
from django.forms import TextInput, NumberInput, Select, ClearableFileInput, EmailInput
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from localflavor.it.forms import ITSocialSecurityNumberField, ITVatNumberField

from invoices.models import *
from invoices.widgets import ITPhoneNumberField, AddressFormField

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        widgets = {
            'catalog': Select(attrs={'class': 'form-control'}),
            'customer': Select(attrs={'class': 'form-control'}),
            }

        exclude = ('invoiced', 'lastchange_by')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('order',)

        widgets = {
            'price': Select(attrs={'class': 'form-control'}),
            'pieces': NumberInput(attrs={'class': 'form-control'}),
            }

    def clean(self):
        # Check that items put in an order are not more than avaiable pieces in stock and than avaialable in the order
        cleaned_data = super(ItemForm, self).clean()
        previous_pieces = self.instance.pieces if self.instance.pieces else 0
        pieces = cleaned_data.get("pieces")
        price = cleaned_data.get("price")
        tot_qty = price.product.quantity + previous_pieces
        if pieces > tot_qty:
            data = { 'pieces': pieces, 'tot_qty': tot_qty }
            raise forms.ValidationError(_("Value %(pieces)s exceed quantity available for this product: %(tot_qty)s") % data)
        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice

        widgets = {
            'payment_type': Select(attrs={'class': 'form-control'}),
            'heading_type': Select(attrs={'class': 'form-control'}),
            }

        fields = ('payment_type', 'heading_type')


class HeadingForm(forms.ModelForm):
    tax_code = ITVatNumberField(label=_('Tax code or Vat code'), widget=TextInput(attrs={'class': 'form-control'}))
    phone = ITPhoneNumberField(label=_('Phone'), widget=TextInput(attrs={'class': 'form-control'}))
    address = AddressFormField(label=_('Address'))

    class Meta:
        model = InvoiceHeading
        exclude = ('lastchange', 'lastchange_by')

        widgets = {
            'short_name': TextInput(attrs={'class': 'form-control'}),
            'long_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'usual_title_respect': TextInput(attrs={'class': 'form-control'}),
            'logo_file': ClearableFileInput(attrs={'class': 'form-control'}),
        }
