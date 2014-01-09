# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import Signal, receiver

product_warning_depletion = Signal(providing_args=["left"])
product_danger_depletion = Signal(providing_args=["left"])

def product_warning_handler(sender, **kwargs):
    print 'product_warning_handler'

def product_danger_handler(sender, **kwargs):
    print 'product_danger_handler'

product_warning_depletion.connect(product_warning_handler)
product_danger_depletion.connect(product_danger_handler)

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
        if self.quantity < self.wrn_tsh:
            return 'danger'
        if self.quantity - self.wrn_tsh > self.wrn_tsh:
            return 'success'
        if self.quantity - self.wrn_tsh < self.wrn_tsh:
            return 'warning'

    @property
    def qty_percentage(self):
        if self.quantity == 0:
            return 1
        tot = 4 * self.wrn_tsh
        return int(100*float(self.quantity) / float(tot))

    @property
    def packages_left(self):
        try:
            return (self.quantity / self.package.size, self.quantity % self.package.size)
        except Exception, e:
            return ('N/A', self.quantity)

    def sell(self, pieces):
        try:
            self.quantity = self.quantity - pieces

            if self.status == 'warning':
                product_warning_depletion.send(sender=self, left=self.quantity)

            if self.status == 'danger':
                product_danger_depletion.send(sender=self, left=self.quantity)

            self.save()
        except Exception, e:
            print e

    def release(self, pieces):
        print 'release'
        self.quantity = self.quantity + pieces
        self.save()
        return self.quantity

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

    def load(self, num_pkg):
        self.product.quantity += num_pkg*self.size
        self.save()
        return self.quantity

    def unload(self, num_pkg):
        self.product.quantity -= num_pkg*self.size
        self.save()
        return self.quantity
