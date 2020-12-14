from django.db import models
from django.utils.translation import ugettext as _

from invoices.modelfields import AddressField


class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    surname = models.CharField(_("Surname"), max_length=200)
    address = AddressField(_("Address"))
    tax_code = models.CharField(_("Tax code"), max_length=200, null=True, blank=True)
    vat_code = models.CharField(_("Vat code"), max_length=200, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=200)
    email = models.EmailField(_("Email"), max_length=200)

    lastchange_by = models.ForeignKey(
        "accounts.UserProfile",
        related_name="customer_edited",
        verbose_name=_("Last change by"),
        null=True,
        on_delete=models.SET_NULL,
    )

    record_date = models.DateTimeField(_("Recorded on"), auto_now_add=True)
    lastchange = models.DateTimeField(_("Last change on"), auto_now_add=True)

    def __unicode__(self):
        return "%s %s" % (self.surname, self.name)

    class Meta:
        ordering = ["surname", "name"]
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        get_latest_by = "surname"
        unique_together = ("tax_code", "vat_code")
