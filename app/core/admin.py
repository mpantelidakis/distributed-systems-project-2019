from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):

    # Order items by id
    ordering = ['id']

    # list items by email and name
    list_display = ['email', 'name']

    # adds some fields to the django admin page so it supports
    # our custom user model
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # when providing a single field, use a comma after so django doesn't
        # treat it as a string
        (
            _('Personal Info'),
            {'fields': ('name',)}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            _('Important dates'),
            {'fields': ('last_login',)}
        )
    )
    # fields in our add user admin page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

# register the tag models to the admin
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Tag)
admin.site.register(models.UploadedImage)
admin.site.register(models.Gallery)

