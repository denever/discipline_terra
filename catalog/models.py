from django.db import models
from django.utils.translation import ugettext as _
from decimal import *

# Create your models here.
class Catalog(models.Model):
    title = models.CharField(_('Title'), max_length=200, unique=True)

    class Meta:
        verbose_name = _('Catalog')
        verbose_name_plural = _('Catalogs')

    @property
    def price_count(self):
        return self.price_set.count()

    def __unicode__(self):
        return self.title

class Price(models.Model):
    catalog = models.ForeignKey(Catalog,
                                verbose_name=_('Catalog'))
    product = models.ForeignKey('stock.Product',
                                verbose_name=_('Product'))
    price_in = models.DecimalField(_('Price IN'), max_digits=10, decimal_places=2)
    vat_in = models.FloatField(_('VAT IN'))
    gain_percentage = models.FloatField(_('Gain'))
    vat_out = models.FloatField(_('VAT OUT'))

    lastchange_by = models.ForeignKey('accounts.UserProfile',
                                      related_name='price_edited',
                                      verbose_name=_('Last change by'))
    lastchange = models.DateTimeField(_('Last change on'), auto_now_add=True)

    class Meta:
        ordering = ['product']
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
        unique_together = (('catalog', 'product'))

    def __unicode__(self):
        return _('Price of %(product)s: %(price_out)s') % {'product':self.product, 'price_out':self.price_out}

    @property
    def price_out(self):
        getcontext().prec = 3
        getcontext().rounding = ROUND_UP
        tot_in = self.price_in + self.price_in*(Decimal(self.vat_in)/Decimal(100))
        gain = (Decimal(self.gain_percentage) + Decimal(self.vat_out))/Decimal(100)
        return tot_in + tot_in*gain
