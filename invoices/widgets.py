# encoding: utf-8

import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.fields import Field, RegexField, Select
from django.contrib.localflavor.it.forms import ITZipCodeField
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class AddressWidget(forms.MultiWidget):
    class Media:
    def __init__(self, attrs=None):
	widgets = (
	    forms.widgets.TextInput(attrs={'placeholder':'Via/Piazza'}),
	    forms.widgets.TextInput(attrs={'placeholder':'Numero Civico'}),
	    forms.widgets.TextInput(attrs={'placeholder':'CAP'}),
	    forms.widgets.TextInput(attrs={'placeholder':'Comune'}),
	    forms.widgets.TextInput(attrs={'placeholder':'Provincia'}),
	    )

	super(AddressWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
	if value:
	    return value.decompress()
	else:
	    return ['','','','','']

    def render(self, name, value, attrs=None):
	print name
	output = [super(AddressWidget, self).render(name, value, attrs)]
	output.append(self.js_script % ( reverse('cap'),
					 name+'_2',
					 name+'_3',
					 name+'_4'))
	return mark_safe(u''.join(output))

class AddressFormField(forms.MultiValueField):
    widget = AddressWidget

    def __init__(self, *args, **kwargs):
	fields = (
	    forms.CharField(label='Via/Piazza'),
	    forms.CharField(label='Numero Civico'),
	    ITZipCodeField(label='CAP'),
	    forms.CharField(label='Comune'),
	    forms.CharField(label='Provincia'),
	    )
	super(AddressFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
	return ','.join(data_list)
