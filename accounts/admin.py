from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from accounts import models
from order.admin import QuoteInline, InvoiceInline

User = get_user_model()

from django.contrib import admin
import jdatetime


class BaseAdmin(admin.ModelAdmin):

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
    search_fields = ('id',)
    ordering = ('-id',)


class UserAdmin(_UserAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'username', 'email', 'display_create_date', 'display_update_date')
    search_fields = BaseAdmin.search_fields + ('email', 'last_name')
    inlines = (QuoteInline, InvoiceInline)

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


admin.site.register(User, UserAdmin)


class CompanyAdmin(BaseAdmin):
    list_display = ('id', 'name', 'owner', 'city', 'industry', 'is_active') + BaseAdmin.list_display
    search_fields = BaseAdmin.search_fields + ('name',)
    inlines = (QuoteInline, InvoiceInline)


admin.site.register(models.Company, CompanyAdmin)
