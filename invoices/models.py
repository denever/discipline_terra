from django.db import models
from django.utils.translation import ugettext as _
from invoices.modelfields import AddressField

# Create your models here.
class Customer(models.Model):
    name = models.CharField(_('name'), max_length=200)
    surname = models.CharField(_('Surname'), max_length=200)
    address = AddressField(_('Address'))
    tax_code = models.CharField(_('Tax code'), max_length=200, blank=True)
    vat_code = models.CharField(_('Vat code'), max_length=200, blank=True)
    phone = models.CharField(_('Phone'), max_length=200)
    email = models.EmailField(_('Email'), max_length=200)

    lastupdate_by = models.ForeignKey('accounts.UserProfile',
                                    related_name='customer_edited',
                                    verbose_name=_('Last update by'))
    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.surname, self.name)

    class Meta:
        ordering = ['surname', 'name']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        get_latest_by = 'surname'

class Item(models.Model):
    order = models.ForeignKey('invoices.Order',
                                verbose_name=_('Order'))
    price = models.ForeignKey('catalog.Price',
                              verbose_name=_('Product'))
    pieces = models.IntegerField(_('Pieces'))

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Item')
        unique_together = ('order','price')
    @property
    def value(self):
        return float(self.pieces * self.price.price_out)

class Order(models.Model):
    customer = models.ForeignKey(Customer,
                                verbose_name=_('Customer'))

    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __unicode__(self):
        return _('Order of %s on %s: ') % (self.customer, self.record_date)

    @property
    def item_count(self):
        total = int()
        for item in self.item_set.all():
            total += item.pieces
        return total

    @property
    def total_value(self):
        total = float(0.0)
        for item in self.item_set.all():
            total += item.value
        return total
