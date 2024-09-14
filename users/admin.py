from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'created_at', 'updated_at')
    list_filter = ('role', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'role')
    ordering = ('created_at',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address', 'phone_number', 'role', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(CustomUser, CustomUserAdmin)
