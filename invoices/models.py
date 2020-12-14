from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from invoices.modelfields import AddressField


class Item(models.Model):
    order = models.ForeignKey(
        "invoices.Order", verbose_name=_("Order"), on_delete=models.CASCADE
    )
    price = models.ForeignKey("catalog.Price", verbose_name=_("Product"))
    pieces = models.PositiveIntegerField(_("Pieces"))
    record_date = models.DateTimeField(_("Recorded on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Item")
        unique_together = ("order", "price")
        ordering = ["record_date"]

    @property
    def amount(self):
        return Decimal(self.pieces) * self.price.price_out

    @property
    def amount_novat(self):
        return Decimal(self.pieces) * self.price.unit_price

    @property
    def as_packages(self):
        try:
            packages = self.pieces / self.price.product.package.size
            spare_pieces = self.pieces % self.price.product.package.size
            if packages != 0:
                return (packages, spare_pieces)
            else:
                return "N/A"
        except Exception:
            return ("N/A", self.pieces)

    def __unicode__(self):
        return self.price.product.__unicode__()


class Order(models.Model):
    catalog = models.ForeignKey("catalog.catalog", verbose_name=_("Catalog"))

    customer = models.ForeignKey("customers.Customer", verbose_name=_("Customer"))

    record_date = models.DateTimeField(_("Recorded on"), auto_now_add=True)
    lastchange_by = models.ForeignKey(
        "accounts.UserProfile",
        related_name="order_edited",
        verbose_name=_("Last change by"),
    )
    lastchange = models.DateTimeField(_("Last change on"), auto_now_add=True)

    invoiced = models.BooleanField(_("Invoiced"), default=False)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["record_date"]

    def __unicode__(self):
        data = {"customer": self.customer, "record_date": self.record_date}
        return _("Order from %(customer)s on %(record_date)s: ") % data

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


class Payment(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __unicode__(self):
        return self.name

    @property
    def amount(self):
        total = Decimal(0.0)
        for invoice in self.invoices_paid.all():
            total += invoice.amount
        return total

    @property
    def amount_novat(self):
        total = Decimal(0.0)
        for invoice in self.invoices_paid.all():
            total += invoice.amount_novat
        return total


class InvoiceHeading(models.Model):
    short_name = models.CharField(_("Name"), max_length=200)
    long_name = models.CharField(_("Full name"), max_length=200)
    address = AddressField(_("Address"))
    tax_code = models.CharField(_("Tax code or Vat code"), max_length=200)
    phone = models.CharField(_("Phone"), max_length=200)
    email = models.EmailField(_("Email"), max_length=200)
    logo_filename = models.FileField(
        _("Logo file"), upload_to="logos", null=True, blank=True
    )
    usual_title_respect = models.CharField(_("Usual title respect"), max_length=200)
    lastchange_by = models.ForeignKey(
        "accounts.UserProfile",
        related_name="invoice_headings_edited",
        verbose_name=_("Last change by"),
    )
    lastchange = models.DateTimeField(_("Last change on"), auto_now_add=True)

    class Meta:
        verbose_name = _("Invoce Heading")
        verbose_name_plural = _("Invoice Headings")

    def __unicode__(self):
        return self.short_name

    def heading_note(self):
        return (
            self.long_name,
            "%s - tel: %s - email: %s" % (self.address, self.phone, self.email),
            "Tax code and Vat code: %s" % self.tax_code,
        )


class Invoice(models.Model):
    customer = models.ForeignKey("customers.Customer", verbose_name=_("Customer"))
    date = models.DateTimeField(_("Invoiced on"), auto_now_add=True)
    issuer = models.ForeignKey(
        "accounts.UserProfile",
        related_name="invoices_issued",
        verbose_name=_("Issued by"),
    )
    payment_type = models.ForeignKey(
        Payment, related_name="invoices_paid", verbose_name=_("Payment type")
    )

    heading_type = models.ForeignKey(
        InvoiceHeading, related_name="invoices_entitled", verbose_name=_("Invoice as")
    )

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        ordering = ["date"]

    def __unicode__(self):
        data = {"customer": self.customer, "date": self.date}
        return _("Invoice for %(customer)s on %(date)s: ") % data

    @property
    def voice_count(self):
        total = int()
        for voice in self.voice_set.all():
            total += voice.pieces
        return total

    @property
    def amount_novat(self):
        total = Decimal(0.0)
        for voice in self.voice_set.all():
            total += voice.amount_novat
        return total

    @property
    def amount(self):
        total = Decimal(0.0)
        for voice in self.voice_set.all():
            total += voice.amount
        return total

    @property
    def tax_rates_used(self):
        """Returns a list of all vat used for this invoice"""
        value_set = set(self.voice_set.values_list("vat"))
        return [vat[0] for vat in value_set]

    def voices_by_vat(self, vat):
        """Returns a queryset of voices by their vat"""
        return self.voice_set.filter(vat=vat)

    def amount_by_vat(self, vat):
        """Returns the amount for each vat"""
        total = Decimal(0.0)
        for voice in self.voices_by_vat(vat):
            total += voice.amount
        return total


class Voice(models.Model):
    invoice = models.ForeignKey("invoices.Invoice", verbose_name=_("Invoice"))

    description = models.CharField(_("Description"), max_length=200)
    unit_price_novat = models.DecimalField(
        _("Unit price"), max_digits=10, decimal_places=2
    )
    unit_price = models.DecimalField(_("Unit price"), max_digits=10, decimal_places=2)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    amount_novat = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    pieces = models.PositiveIntegerField(_("Pieces"))
    vat = models.DecimalField(_("VAT"), max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = _("Voice")
        verbose_name_plural = _("Voices")

    def __unicode__(self):
        return "%s %s %s %s" % (
            self.description,
            self.pieces,
            self.unit_price,
            self.amount,
        )


@receiver(pre_delete, sender=Item)
def pre_delete_item(sender, **kwargs):
    instance = kwargs["instance"]
    # avoid to release items for an invoiced order
    if not instance.order.invoiced:
        instance.price.product.release(instance.pieces)
