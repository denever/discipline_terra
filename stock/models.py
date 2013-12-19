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

    lastupdate_by = models.ForeignKey('accounts.UserProfile',
                                    related_name='companies_edited',
                                    verbose_name=_('Last update by'))
    lastupdate = models.DateTimeField(_('Last update on'), auto_now_add=True)


    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['code']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
