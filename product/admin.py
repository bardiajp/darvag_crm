import jdatetime
from django.contrib import admin
from django.db import transaction
from django.db.models import Sum

from .models import Item, Product, ProductCategory, ProductGroup, PriceBook, Package


# ---- InLInes ----

class ItemInline(admin.StackedInline):
    model = Item
    extra = 0
    readonly_fields = ('total_price', 'invoice')


# ---- Admin Panels ----
class BaseProductAdmin(admin.ModelAdmin):

    def display_create_date(self, obj):
        if obj.created_at:
            jalali_date = jdatetime.date.fromgregorian(date=obj.created_at)
            return jalali_date.strftime('%Y-%m-%d')
        return "-"

    def display_update_date(self, obj):
        if obj.updated_at:
            jalali_date = jdatetime.date.fromgregorian(date=obj.updated_at)
            return jalali_date.strftime('%Y-%m-%d')
        return "-"

    display_create_date.short_description = 'Created At'
    display_update_date.short_description = 'Updated At'

    list_display = ('display_create_date', 'display_update_date')
    readonly_fields = ('display_create_date', 'display_update_date')
    ordering = ('-id',)


@admin.register(ProductCategory)
class ProducerCategoryAdmin(BaseProductAdmin):
    list_display = ('id', 'name', 'parent_category') + BaseProductAdmin.list_display
    list_filter = ('id', 'name') + BaseProductAdmin.list_filter
    search_fields = ('id', 'name') + BaseProductAdmin.search_fields


@admin.register(ProductGroup)
class ProducerGroupAdmin(BaseProductAdmin):
    list_display = ('id', 'name', 'parent_group') + BaseProductAdmin.list_display
    list_filter = ('id', 'name') + BaseProductAdmin.list_filter
    search_fields = ('id', 'name') + BaseProductAdmin.search_fields


@admin.register(Product)
class ProductAdmin(BaseProductAdmin):
    list_display = ('id', 'category', 'name', 'code', 'price', 'unit', 'is_active') + BaseProductAdmin.list_display
    list_filter = ('id', 'name') + BaseProductAdmin.list_filter
    search_fields = ('id', 'name') + BaseProductAdmin.search_fields


@admin.register(PriceBook)
class PriceBookAdmin(BaseProductAdmin):
    list_display = ('id', 'name', 'price', 'discount') + BaseProductAdmin.list_display
    list_filter = ('name',) + BaseProductAdmin.list_filter
    search_fields = ('name',) + BaseProductAdmin.search_fields


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit_price', 'total_price', 'starts_at', 'ends_at')
    list_filter = ('id', 'name', 'starts_at')
    search_fields = ('id', 'name')
    ordering = ('-starts_at',)
    inlines = (ItemInline,)

    def ends_at(self, obj):
        if obj.starts_at:
            ends_at = obj.duration + obj.starts_at
            return ends_at

    def save_model(self, request, obj, form, change):
        print('in save')
        with transaction.atomic():
            sum = obj.items.all().aggregate(Sum('total_price'))['total_price__sum']
            obj.unit_price = sum
            obj.total_price = obj.unit_price * obj.duration.days
            obj.save()


@admin.register(Item)
class ItemAdmin(BaseProductAdmin):
    list_display = ('id', 'quote', 'invoice', 'product', 'item_price', 'total_price') + BaseProductAdmin.list_display
    readonly_fields = ("total_price",)
    list_filter = ('quote', 'invoice', 'product') + BaseProductAdmin.list_filter
    search_fields = ('quote', 'invoice', 'product') + BaseProductAdmin.search_fields

    def save_model(self, request, obj, form, change):

        with transaction.atomic():
            if obj.product and not obj.item_price:
                obj.item_price = obj.product.price
                obj.total_price = obj.product.price * obj.quantity
            elif obj.item_price:
                obj.total_price = obj.item_price * obj.quantity

            super().save_model(request, obj, form, change)
