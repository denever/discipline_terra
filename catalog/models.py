from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Price(models.Model):
    product = models.ForeignKey('stock.Product',
                                verbose_name=_('Product'), unique=True)
    price_in = models.FloatField(_('Price IN'))
    vat_in = models.FloatField(_('VAT IN'))
    gain_percentage = models.FloatField(_('Gain'))
    vat_out = models.FloatField(_('VAT OUT'))

    lastupdate_by = models.ForeignKey('accounts.UserProfile',
                                      related_name='price_edited',
                                      verbose_name=_('Last update by'))
    lastupdate = models.DateTimeField(_('Last update on'), auto_now_add=True)

    class Meta:
        ordering = ['product']
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __unicode__(self):
        return _('Price of %s: ') % (self.product, self.price_out)

    def price_out(self):
        tot_in = float(self.price_in + self.price_in*(self.vat_in/100))
        return float(tot_in + tot_in*(self.gain_percentage + self.vat_out)/100)
