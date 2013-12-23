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

class Cart(models.Model):
    order = models.ForeignKey('invoices.Order',
                                verbose_name=_('Order'), unique=True)
    price = models.ForeignKey('catalog.Price',
                              verbose_name=_('Product'), unique=True)
    pieces = models.IntegerField(_('Pieces'))

    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

class Order(models.Model):
    customer = models.ForeignKey(Customer,
                                verbose_name=_('Customer'), unique=True)

    items = models.ManyToManyField('catalog.Price', through='Cart')

    record_date = models.DateTimeField(_('Recorded on'), auto_now_add=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __unicode__(self):
        return _('Order of %s on %s: ') % (self.customer, self.record_date)
