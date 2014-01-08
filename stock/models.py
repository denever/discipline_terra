# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Product(models.Model):
    code = models.CharField(_('Code'), max_length=200, unique=True)
    description = models.CharField(_('Description'), max_length=200)
    quantity = models.PositiveIntegerField(_('Quantity'))
    producer = models.CharField(_('Producer'), max_length=200)
    wrn_tsh =  models.PositiveIntegerField(_('Warning Threshold'))
    barcode = models.PositiveIntegerField(_('Barcode'), max_length=200)

    lastupdate_by = models.ForeignKey('accounts.UserProfile',
                                    related_name='products_edited',
                                    verbose_name=_('Last update by'))
    lastupdate = models.DateTimeField(_('Last update on'), auto_now_add=True)


    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ['code']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    @property
    def status(self):
        if self.quantity == 0:
            return 'danger'
        if self.quantity < self.wrn_tsh:
            return 'danger'
        if self.quantity - self.wrn_tsh > self.wrn_tsh:
            return 'success'
        if self.quantity - self.wrn_tsh < self.wrn_tsh:
            return 'warning'

    @property
    def qty_percentage(self):
        tot = 4 * self.wrn_tsh
        return int(100*float(self.quantity) / float(tot))

    @property
    def packages_left(self):
        try:
            return (self.quantity / self.package.size, self.quantity % self.package.size)
        except Exception, e:
            return ('N/A', self.quantity)

class Package(models.Model):
    product = models.OneToOneField(Product, verbose_name=_('Product'), unique=True)
    size = models.PositiveIntegerField(_('Package size'))
    barcode = models.PositiveIntegerField(_('Barcode'), max_length=200)

    lastupdate_by = models.ForeignKey('accounts.UserProfile',
                                    related_name='packages_edited',
                                    verbose_name=_('Last update by'))
    lastupdate = models.DateTimeField(_('Last update on'), auto_now_add=True)

    def __unicode__(self):
        return _('Package of %s') % (self.product)

    class Meta:
        ordering = ['product']
        verbose_name = _('Package')
        verbose_name_plural = _('Packages')
