from django.db import models
from django.utils.translation import gettext as _

from order.models import Quote, Invoice


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(BaseModel):
    name = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('Description'), max_length=500, null=False, blank=False)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'category'

    def __str__(self):
        return f'{self.name}'


class ProductGroup(BaseModel):
    name = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('Description'), max_length=500, null=False, blank=False)
    parent_group = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        db_table = 'group'

    def __str__(self):
        return f'{self.name} - {self.parent_group}'


class Product(BaseModel):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(ProductGroup, on_delete=models.SET_NULL, null=True, blank=True)
    parent_product = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=500, null=False, blank=False)
    price = models.IntegerField(_('Price'), null=True, blank=True)
    product_no = models.CharField(_('Product No'), max_length=50, null=False, blank=False)
    description = models.TextField(_('Description'), max_length=500, null=False, blank=False)
    stock = models.PositiveIntegerField(_('Stock'), default=1)
    tax = models.DecimalField(_('Tax'), default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    image = models.ImageField(_('Image'), null=True, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        db_table = 'product'

    def __str__(self):
        return f'{self.name}'


class PriceBook(BaseModel):
    name = models.CharField(_('Name'), max_length=50, null=False, blank=False)
    price = models.DecimalField(_('Price'), default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(_('Discount'), default=0, max_digits=20, decimal_places=2, null=True,
                                   blank=True)

    class Meta:
        verbose_name = _('Price Book')
        verbose_name_plural = _('Price Books')
        db_table = 'price_book'

    def __str__(self):
        return f'{self.name} - {self.price}'


class Item(BaseModel):
    quote = models.ForeignKey(Quote, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    item_price = models.DecimalField(_('Price'), default=0, max_digits=20, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(_('Total Price'), default=0, max_digits=20, decimal_places=2, null=True,
                                      blank=True)
    price_book = models.ForeignKey(PriceBook, on_delete=models.SET_NULL, null=True, blank=True)
    period = models.IntegerField(null=True, blank=True)
    comment = models.TextField(_('Comment'), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        db_table = 'item'

    def __str__(self):
        return f'{self.id} - {self.quantity}'
