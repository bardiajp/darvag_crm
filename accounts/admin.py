from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from accounts import models
from order.admin import QuoteInline, InvoiceInline

User = get_user_model()


class BaseAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('id',)
    ordering = ('-id',)


class UserAdmin(_UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'age') + BaseAdmin.list_display
    search_fields = BaseAdmin.search_fields + ('email', 'last_name')
    inlines = (QuoteInline, InvoiceInline)


admin.site.register(User, UserAdmin)


class CompanyAdmin(BaseAdmin):
    list_display = ('id', 'name', 'owner', 'city', 'industry', 'is_active') + BaseAdmin.list_display
    search_fields = BaseAdmin.search_fields + ('name',)
    inlines = (QuoteInline, InvoiceInline)


admin.site.register(models.Company, CompanyAdmin)
