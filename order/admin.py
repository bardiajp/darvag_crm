from django.urls import reverse

import jdatetime
from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html

from product.admin import ItemInline
from .models import Quote, Invoice, Potential
from .views import QuoteView


# ---- InLInes ----

class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 1


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 1


# ---- Admin Panels ----

class BaseOrderAdmin(admin.ModelAdmin):

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
    ordering = ('id',)
    search_fields = ('id',)


@admin.register(Potential)
class PotentialAdmin(BaseOrderAdmin):
    list_display = ('id', 'name', 'status') + BaseOrderAdmin.list_display
    search_fields = ('id', 'name', 'user__username', 'company__name') + BaseOrderAdmin.search_fields


@admin.register(Quote)
class QuoteAdmin(BaseOrderAdmin):
    list_display = ('id', 'subject', 'stage', 'status', 'total_price', 'discount',
                    'display_discount_rate', 'final_price', 'quote_details',
                    'is_active') + BaseOrderAdmin.list_display
    search_fields = BaseOrderAdmin.search_fields + ('subject', 'stage', 'status')
    list_filter = ('id', 'status', 'stage', 'is_active') + BaseOrderAdmin.list_filter
    readonly_fields = ("total_price", "final_price")
    inlines = (ItemInline,)
    exclude = ("price_after_discount",)

    def quote_details(self, obj):
        url = f"/quote-details/{obj.id}"
        return format_html("<a target='_blank' class='btn btn-primary' href='{}'>Details</a>", url)

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
        total_price = 0
        try:
            total_price = sum(item.total_price for item in obj.items.all())
            obj.total_price = total_price
        except:
            pass

        obj.total_price = total_price

        if obj.discount is not None and obj.discount > 0:
            discount_amount = obj.discount
        elif obj.discount_rate is not None and obj.discount_rate > 0:
            discount_amount = (total_price * obj.discount_rate ) / 100
            obj.discount = discount_amount
        else:
            discount_amount = 0

        obj.price_after_discount = total_price - discount_amount
        if obj.tax is not None:
            obj.final_price = obj.price_after_discount + (obj.price_after_discount * obj.tax / 100)
        else:
            obj.final_price = obj.price_after_discount

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            self.calculate_final_price(obj)
            super().save_model(request, obj, form, change)

    def display_discount_rate(self, obj):
        print(f'{obj.discount=} {obj.total_price=}')
        if obj.discount_rate:
            return f'{obj.discount_rate:.2f}%'
        elif obj.discount:
            return f'{(float(obj.discount) / float(obj.total_price or 1)) * 100:.2f}%'
        else:
            return ''

    display_discount_rate.short_description = 'Discount rate'


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
