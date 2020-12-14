# encoding: utf-8
from django.db import models
from django.dispatch import Signal
from django.utils.translation import ugettext as _

# from django.db.models.signals import pre_save, post_save, pre_delete
# , receiver

product_warning_depletion = Signal(providing_args=["left"])
product_danger_depletion = Signal(providing_args=["left"])
product_depleted = Signal()


def product_warning_handler(sender, **kwargs):
    print("product_warning_handler")


def product_danger_handler(sender, **kwargs):
    print("product_danger_handler")


def product_depleted_handler(sender, **kwargs):
    print("product_depleted_handler")


product_warning_depletion.connect(product_warning_handler)
product_danger_depletion.connect(product_danger_handler)
product_depleted.connect(product_depleted_handler)


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)
    description = models.CharField(_("Description"), max_length=200)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), on_delete=models.CASCADE
    )
    code = models.CharField(_("Code"), max_length=200, unique=True)
    description = models.CharField(_("Description"), max_length=200)
    quantity = models.PositiveIntegerField(_("Quantity"))
    producer = models.CharField(_("Producer"), max_length=200)
    wrn_tsh = models.PositiveIntegerField(_("Warning Threshold"))
    barcode = models.PositiveIntegerField(_("Barcode"))

    lastchange_by = models.ForeignKey(
        "accounts.UserProfile",
        related_name="products_edited",
        verbose_name=_("Last change by"),
        null=True,
        on_delete=models.SET_NULL,
    )
    lastchange = models.DateTimeField(_("Last change on"), auto_now_add=True)

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ["code"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    @property
    def status(self):
        if self.quantity < self.wrn_tsh:
            return "danger"
        if self.quantity - self.wrn_tsh > self.wrn_tsh:
            return "success"
        if self.quantity - self.wrn_tsh < self.wrn_tsh:
            return "warning"

    @property
    def qty_percentage(self):
        if self.quantity == 0:
            return 1
        tot = 4 * self.wrn_tsh
        return int(100 * float(self.quantity) / float(tot))

    @property
    def packages_left(self):
        try:
            return (
                self.quantity / self.package.size,
                self.quantity % self.package.size,
            )
        except Exception:
            return ("N/A", self.quantity)

    def sell(self, pieces):
        try:
            self.quantity = self.quantity - pieces

            if self.status == "warning":
                product_warning_depletion.send(sender=self, left=self.quantity)

            if self.status == "danger":
                product_danger_depletion.send(sender=self, left=self.quantity)
                if self.quantity == 0:
                    product_depleted.send(sender=self)

            self.save()
        except Exception as e:
            print(e)

    def release(self, pieces):
        self.quantity = self.quantity + pieces
        self.save()
        return self.quantity


class Package(models.Model):
    product = models.OneToOneField(
        Product, verbose_name=_("Product"), unique=True, on_delete=models.CASCADE
    )
    size = models.PositiveIntegerField(_("Package size"))
    barcode = models.PositiveIntegerField(_("Barcode"))
    lastchange_by = models.ForeignKey(
        "accounts.UserProfile",
        related_name="packages_edited",
        verbose_name=_("Last change by"),
        null=True,
        on_delete=models.SET_NULL,
    )
    lastchange = models.DateTimeField(_("Last change on"), auto_now_add=True)

    def __unicode__(self):
        return _("Package of %s") % (self.product)

    class Meta:
        ordering = ["product"]
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")

    def load(self, num_pkg):
        self.product.quantity += num_pkg * self.size
        self.save()
        return self.quantity

    def unload(self, num_pkg):
        self.product.quantity -= num_pkg * self.size
        self.save()
        return self.quantity
