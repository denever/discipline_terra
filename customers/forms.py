from django import forms
from django.forms import EmailInput, TextInput
from django.utils.translation import ugettext as _
from invoices.widgets import AddressFormField, ITPhoneNumberField
from localflavor.it.forms import ITSocialSecurityNumberField, ITVatNumberField

from .models import Customer


class CustomerForm(forms.ModelForm):
    tax_code = ITSocialSecurityNumberField(
        label=_("Tax code"),
        widget=TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    vat_code = ITVatNumberField(
        label=_("Vat code"),
        widget=TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    phone = ITPhoneNumberField(
        label=_("Phone"), widget=TextInput(attrs={"class": "form-control"})
    )
    address = AddressFormField(label=_("Address"))

    class Meta:
        model = Customer
        exclude = ("lastchange", "lastchange_by")

        widgets = {
            "surname": TextInput(attrs={"class": "form-control"}),
            "name": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super(CustomerForm, self).clean()

        tax_code = cleaned_data.get("tax_code")
        vat_code = cleaned_data.get("vat_code")

        if tax_code and vat_code:  # both were entered
            raise forms.ValidationError(_("Enter only one of tax code or vat code"))
        elif not tax_code and not vat_code:  # neither were entered
            raise forms.ValidationError(_("You must enter a tax code or a vat code"))

        return cleaned_data
