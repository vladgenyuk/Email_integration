from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import EmailUserAccount, EmailMessage

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email_login', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_login', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    list_display = ('id', 'email_login', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email_login', 'first_name', 'last_name')
    ordering = ('email_login',)
    filter_horizontal = []


class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email_service', 'from_email', 'to_email', 'subject', 'sent_at', 'received_at', 'attachments', 'body')
    list_display_links = ('id', 'user')
    search_fields = ('subject', 'user')
    fields = ('id', 'user', 'email_service', 'from_email', 'to_email', 'subject', 'sent_at', 'received_at', 'attachments', 'body')


admin.site.register(EmailMessage, EmailMessageAdmin)
admin.site.register(EmailUserAccount, UserAdmin)
admin.site.unregister(Group)
