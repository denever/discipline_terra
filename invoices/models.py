from decimal import *

from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import Signal, receiver

from invoices.modelfields import AddressField

# Create your models here.
class Customer(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    surname = models.CharField(_('Surname'), max_length=200)
    address = AddressField(_('Address'))
    tax_code = models.CharField(_('Tax code'), max_length=200, null=True, blank=True)
    vat_code = models.CharField(_('Vat code'), max_length=200, null=True, blank=True)
    phone = models.CharField(_('Phone'), max_length=200)
    email = models.EmailField(_('Email'), max_length=200)

    lastchange_by = models.ForeignKey('accounts.UserProfile',
                                    related_name='customer_edited',
                                    verbose_name=_('Last change by'))

    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)
    lastchange = models.DateTimeField(_('Last change on'), auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.surname, self.name)

    class Meta:
        ordering = ['surname', 'name']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        get_latest_by = 'surname'
        unique_together = ('tax_code','vat_code')

class Item(models.Model):
    order = models.ForeignKey('invoices.Order',
                                verbose_name=_('Order'), on_delete=models.CASCADE)
    price = models.ForeignKey('catalog.Price',
                              verbose_name=_('Product'))
    pieces = models.PositiveIntegerField(_('Pieces'))
    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Item')
        unique_together = ('order','price')
        ordering = ['record_date']

    @property
    def amount(self):
        return Decimal(self.pieces) * self.price.price_out

    @property
    def as_packages(self):
        try:
            packages = self.pieces / self.price.product.package.size
            spare_pieces = self.pieces % self.price.product.package.size
            if packages != 0:
                return (packages, spare_pieces)
            else:
                return 'N/A'
        except Exception, e:
            return ('N/A', self.pieces)

    def __unicode__(self):
        return self.price.product.__unicode__()

class Order(models.Model):
    catalog = models.ForeignKey('catalog.catalog',
                                verbose_name=_('Catalog'))

    customer = models.ForeignKey(Customer,
                                verbose_name=_('Customer'))

    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)
    lastchange_by = models.ForeignKey('accounts.UserProfile',
                                    related_name='order_edited',
                                    verbose_name=_('Last change by'))
    lastchange = models.DateTimeField(_('Last change on'), auto_now_add=True)

    invoiced = models.BooleanField(_('Invoiced'), default=False)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['record_date']

    def __unicode__(self):
        return _('Order from %(customer)s on %(record_date)s: ') % {'customer': self.customer, 'record_date': self.record_date}

    @property
    def item_count(self):
        total = int()
        for item in self.item_set.all():
            total += item.pieces
        return total

    @property
    def amount(self):
        total = Decimal(0.0)
        for item in self.item_set.all():
            total += item.amount
        return total

class Invoice(models.Model):
    customer = models.ForeignKey(Customer,
                                verbose_name=_('Customer'))
    date = models.DateTimeField(_('Invoiced on'), auto_now_add=True)
    issuer = models.ForeignKey('accounts.UserProfile',
                        related_name='invoices_issued',
                        verbose_name=_('Issued by'))

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['date']

    def __unicode__(self):
        return _('Invoice for %(customer)s on %(date)s: ') % {'customer': self.customer, 'date': self.date}

    @property
    def voice_count(self):
        total = int()
        for voice in self.voice_set.all():
            total += voice.pieces
        return total

    @property
    def amount(self):
        total = Decimal(0.0)
        for voice in self.voice_set.all():
            total += voice.amount
        return total

class Voice(models.Model):
    invoice = models.ForeignKey('invoices.Invoice',
                                verbose_name=_('Invoice'))

    description = models.CharField(_('Description'), max_length=200)
    unit_price = models.DecimalField(_('Unit price'), max_digits=10, decimal_places=2)
    amount = models.DecimalField(_('Amount'), max_digits=10, decimal_places=2)
    pieces = models.PositiveIntegerField(_('Pieces'))

    class Meta:
        verbose_name = _('Voice')
        verbose_name_plural = _('Voices')

    def __unicode__(self):
        return '%s %s %s %s' % (self.description, self.pieces, self.unit_price, self.amount)

@receiver(pre_delete, sender=Item)
def pre_delete_item(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.order.invoiced: # avoid to release items for an invoiced order
        instance.price.product.release(instance.pieces)
