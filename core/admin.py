from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from django.contrib.auth.admin import UserAdmin
from core.models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            # 'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff', 'user_permissions', 'groups', )
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'avatar', 'is_staff', 'groups')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user_permissions', 'is_active', 'is_superuser', )
        }),
    )
    list_display = ('username', 'email', 'date_joined')
    list_filter = ('is_staff', 'is_active', )
    search_fields = ('last_name__startswith', )

    class Meta:
        ordering = ('date_joined', )
admin.site.register(User, UserAdmin)

for model in apps.get_app_config('core').get_models():
    try: admin.site.register(model)
    except AlreadyRegistered: pass
