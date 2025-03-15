from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from accounts.models import User, Company


class StatusChoices(models.IntegerChoices):
    DRAFT = 1, _("Draft")
    PENDING = 2, _("Pending")
    APPROVED = 3, _("Approved")
    REJECTED = 4, _("Rejected")
    EXPIRED = 5, _("Expired")
    CONVERTED = 6, _("Converted")
    CANCELLED = 7, _("Cancelled")


class StageChoices(models.IntegerChoices):
    PENDING = 1, _('Pending')
    APPROVED = 2, _('Approved')
    CANCELLED = 3, _('Cancelled')
    SENT = 4, _('Sent')
    PAID = 5, _('Paid')
    EXPIRED = 6, _('Expired')
    PROCESSING_PAYMENT = 7, _('Processing')
    REJECTED = 8, _('Rejected')
    COMPLETED = 9, _('Completed')


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class Potential(BaseModel):
    name = models.CharField(_("Potential name"), max_length=255)
    description = models.CharField(_("Potential description"), max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(_("Potential status"), max_length=255)

    class Meta:
        verbose_name = _("Potential")
        verbose_name_plural = _("Potentials")
        db_table = "potential"

    def __str__(self):
        return f"{self.name} - {self.user.last_name} - {self.company.name} "


class Quote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    potential = models.ForeignKey(Potential, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(_("Quote subject"), max_length=50, null=False, blank=False)
    stage = models.PositiveSmallIntegerField(_("Quote stage"), choices=StageChoices, null=False, blank=False,
                                             default=StageChoices.PENDING.value)
    status = models.PositiveIntegerField(_("Quote status"), choices=StatusChoices, null=False, blank=False,
                                         default=StatusChoices.DRAFT.value)
    address = models.CharField(_("Quote address"), max_length=255, null=False, blank=False)
    description = models.CharField(_("Quote description"), max_length=255, null=False, blank=False)
    terms_conditions = models.CharField(_("Quote terms conditions"), max_length=255, null=False, blank=False)
    is_active = models.BooleanField(_("Quote status"), default=True)
    export_file = models.FileField(_("Quote export file"), null=True, blank=True)
    total_price = models.DecimalField(_("Total price"), max_digits=20, decimal_places=2, null=True, blank=True,
                                      default=0)
    tax = models.DecimalField(_("Tax"), max_digits=20, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(_("Discount"), max_digits=20, decimal_places=2, null=True, blank=True)
    discount_rate = models.IntegerField(_("Discount rate"), null=True, blank=True)
    final_price = models.DecimalField(_("Final price"), max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        db_table = "quote"

    def clean(self):
        super().clean()
        if self.discount is not None and self.discount_rate is not None:
            raise ValidationError(_("You can only set either discount or discount_rate, not both."))
        if self.discount is None and self.discount_rate is None:
            raise ValidationError(_("You must set either discount or discount_rate."))

    def __str__(self):
        return f"{self.id} - {self.user.last_name} - {self.company.name}"


class Invoice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    potential = models.ForeignKey(Potential, on_delete=models.CASCADE)
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)
    invoice_no = models.PositiveIntegerField(_("Invoice number"), null=True, blank=True)
    subject = models.CharField(_("Invoice subject"), max_length=50, null=False, blank=False)
    stage = models.PositiveIntegerField(_("Invoice stage"), choices=StageChoices, null=False, blank=False,
                                        default=StageChoices.PENDING.value)
    status = models.PositiveIntegerField(_("Invoice status"), choices=StatusChoices, null=False, blank=False,
                                         default=StatusChoices.DRAFT.value)
    is_active = models.BooleanField(_("Invoice status"), default=True)
    address = models.CharField(_("Invoice address"), max_length=255, null=False, blank=False)
    description = models.CharField(_("Invoice description"), max_length=255, null=False, blank=False)
    terms_conditions = models.CharField(_("Invoice terms conditions"), max_length=255, null=False, blank=False)
    export_file = models.FileField(_("Invoice export file"), null=True, blank=True)
    total_price = models.DecimalField(_("Total price"), max_digits=20, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(_("Tax"), max_digits=20, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(_("Discount"), max_digits=20, decimal_places=2, null=True, blank=True)
    discount_rate = models.IntegerField(_("Discount rate"), null=True, blank=True)
    final_price = models.DecimalField(_("Final price"), max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        db_table = "invoice"

    def __str__(self):
        return f"{self.id} - {self.user.last_name} - {self.company.name} - {self.is_active}"