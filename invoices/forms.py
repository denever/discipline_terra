from django import forms
from django.forms import TextInput, NumberInput, Select
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404
from localflavor.it.forms import ITSocialSecurityNumberField, ITVatNumberField

from invoices.models import Customer, Order, Item
from invoices.widgets import ITPhoneNumberField, AddressFormField

class CustomerForm(forms.ModelForm):
    tax_code = ITSocialSecurityNumberField(label=_('Tax code'), widget=TextInput(attrs={'class': 'form-control'}), required=False)
    vat_code = ITVatNumberField(label=_('Vat code'), widget=TextInput(attrs={'class': 'form-control'}), required=False)
    phone = ITPhoneNumberField(label=_('Phone'), widget=TextInput(attrs={'class': 'form-control'}))
    address = AddressFormField(label=_('Address'))

    class Meta:
        model = Customer
        exclude = ('lastupdate', 'lastupdate_by')

        widgets = {
            'surname': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(CustomerForm, self).clean()

        tax_code = cleaned_data.get("tax_code")
        vat_code = cleaned_data.get("vat_code")

        if tax_code and vat_code: # both were entered
            raise forms.ValidationError(_("Enter only one of tax code or vat code"))
        elif not tax_code and not vat_code: # neither were entered
            raise forms.ValidationError(_("You must enter a tax code or a vat code"))

        return cleaned_data

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        widgets = {
            'customer': Select(attrs={'class': 'form-control'}),
            }

        exclude = ('invoiced', 'lastupdate_by')

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
            raise forms.ValidationError(_("Value %s exceed quantity available for this product: %s") % (pieces, tot_qty))
        return cleaned_data
