from django.contrib import admin
from django.db import transaction

from .models import Item, Product, ProductCategory, ProductGroup, PriceBook


# ---- InLInes ----

class ItemInline(admin.StackedInline):
    model = Item
    extra = 0
    readonly_fields = ('total_price',)


# ---- Admin Panels ----
class BaseProductAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
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
    list_display = ('id', 'category', 'name', 'price', 'is_active') + BaseProductAdmin.list_display
    list_filter = ('id', 'name') + BaseProductAdmin.list_filter
    search_fields = ('id', 'name') + BaseProductAdmin.search_fields


@admin.register(PriceBook)
class PriceBookAdmin(BaseProductAdmin):
    list_display = ('id', 'name', 'price', 'discount') + BaseProductAdmin.list_display
    list_filter = ('name',) + BaseProductAdmin.list_filter
    search_fields = ('name',) + BaseProductAdmin.search_fields


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
