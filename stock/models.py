# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Product(models.Model):
    code = models.CharField(_('Code'), max_length=200, primary_key=True)
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


class Package(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Product'))
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
