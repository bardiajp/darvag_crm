from django.contrib import admin
from django.db import transaction

from product.admin import ItemInline
from .models import Quote, Invoice, Potential


# ---- InLInes ----

class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 1


# ---- Admin Panels ----

class BaseOrderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    ordering = ('id',)
    search_fields = ('id',)


@admin.register(Potential)
class PotentialAdmin(BaseOrderAdmin):
    list_display = ('id', 'name', 'status') + BaseOrderAdmin.list_display
    search_fields = ('id', 'name', 'user__username', 'company__name') + BaseOrderAdmin.search_fields


@admin.register(Quote)
class QuoteAdmin(BaseOrderAdmin):
    list_display = ('id', 'subject', 'stage', 'status', 'price_per_item', 'total_price', 'discount', 'final_price',
                    'is_active') + BaseOrderAdmin.list_display
    search_fields = BaseOrderAdmin.search_fields + ('subject', 'stage', 'status')
    list_filter = ('id', 'status', 'stage', 'is_active') + BaseOrderAdmin.list_filter
    readonly_fields = ("final_price",)
    inlines = (ItemInline,)

    def save_formset(self, request, form, formset, change):
        with transaction.atomic():
            for form in formset:
                obj = form.instance
                if obj.product and not obj.item_price:
                    obj.total_price = obj.product.price * obj.quantity
                elif obj.item_price:
                    obj.total_price = obj.item_price * obj.quantity
                obj.save()
            super().save_formset(request, form, formset, change)

    @staticmethod
    def calculate_final_price(obj):
        total_price = sum(item.total_price for item in obj.items.all())
        obj.total_price = total_price

        if obj.discount is not None and obj.discount > 0:
            discount_amount = obj.discount
        elif obj.discount_rate is not None and obj.discount_rate > 0:
            discount_amount = (total_price * obj.discount_rate) / 100
            obj.discount = obj.total_price - discount_amount
        else:
            discount_amount = 0

        price_after_discount = total_price - discount_amount
        if obj.tax is not None:
            obj.final_price = price_after_discount + (price_after_discount * obj.tax / 100)
        else:
            obj.final_price = price_after_discount

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            self.calculate_final_price(obj)
            super().save_model(request, obj, form, change)

    def price_per_item(self, obj):
        item_price = sum(item.item_price for item in obj.items.all())
        return item_price

    price_per_item.short_description = 'Price per item'


@admin.register(Invoice)
class InvoiceAdmin(BaseOrderAdmin):
    list_display = ('id', 'subject', 'stage', 'status', 'total_price', 'discount', 'final_price',
                    'is_active') + BaseOrderAdmin.list_display
    search_fields = BaseOrderAdmin.search_fields + ('subject', 'stage', 'status')
    list_filter = ('id', 'status', 'stage', 'is_active') + BaseOrderAdmin.list_filter
    inlines = (ItemInline,)

    def save_model(self, request, obj, form, change):
        if obj.quote:
            obj.total_price = obj.quote.total_price
            obj.discount = obj.quote.discount
            obj.final_price = obj.quote.final_price
        super().save_model(request, obj, form, change)
