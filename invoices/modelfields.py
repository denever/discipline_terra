# encoding: utf-8
import re
from urllib.parse import urlencode

from django.db import models

from invoices.widgets import AddressFormField

addr_re = re.compile(
    r"(?P<street>.+), (?P<number>.+) - (?P<postcode>\d+) (?P<town>\w+) \((?P<province>\w{2})\)"  # noqa: E501
)


class Address(object):
    def __init__(self, street, number, postcode, town, province):
        self.street = street
        self.number = number
        self.postcode = postcode
        self.town = town
        self.province = province

    def __unicode__(self):
        return "%s, %s - %s %s (%s)" % (
            self.street,
            self.number,
            self.postcode,
            self.town,
            self.province,
        )

    def __repr__(self):
        return self.__unicode__()

    def __eq__(self, other):
        if isinstance(other, Address):
            eq = self.street == other.street
            eq = eq and self.number == other.number
            eq = eq and self.postcode == other.postcode
            eq = eq and self.town == other.town
            eq = eq and self.province == other.province
            return eq
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def decompress(self):
        return [self.street, self.number, self.postcode, self.town, self.province]

    def mapurl(self):
        return "http://maps.google.it/maps?" + urlencode(
            {
                "om": "1",
                "iwloc": "addr",
                "f": "q",
                "q": self.__unicode__(),
                "hl": "it",
                "z": "15",
                "ie": "UTF8",
            }
        )


class AddressField(models.Field):
    description = " An address for an office or settlement "

    def __init__(self, *args, **kwargs):
        super(AddressField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return "VARCHAR(255)"

    def from_db_value(self, value, expression, connection, context):
        # TODO
        pass

    def to_python(self, value):
        if isinstance(value, Address):
            return value
        value = str(value)
        match = addr_re.match(value)
        if match:
            return Address(**match.groupdict())
        else:
            return Address(None, None, None, None, None)

    def get_prep_value(self, value):
        return "%s, %s - %s %s (%s)" % (
            value.street,
            value.number,
            value.postcode,
            value.town,
            value.province,
        )

    def formfield(self, **kwargs):
        defaults = {"form_class": AddressFormField}
        defaults.update(kwargs)
        return super(AddressField, self).formfield(**defaults)
