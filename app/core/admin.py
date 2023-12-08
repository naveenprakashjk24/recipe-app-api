'''
Django admin customizations.
'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    ''' define the admin pages for user'''
    ordering = ['id']
    list_display = ['email', 'name', 'is_active',]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields':('last_login',)
            }
        )

    )
    readonly_fields= ['last_login']
    add_fieldsets = (
        (None, {
            'classes':('wide',), # django css concpet for this line.
            'fields':(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
