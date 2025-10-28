# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _
# from .models import User

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = ('email', 'first_name', 'last_name','phone', 'is_active', 'is_staff', 'date_joined')
#     list_filter = ('is_staff', 'is_active', 'is_superuser')

#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         (_('Personal Info'), {'fields': ('first_name', 'last_name','phone')}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'first_name', 'last_name','phone', 'password1', 'is_active', 'is_staff'),
#         }),
#     )

#     search_fields = ('email', 'first_name', 'last_name','phone')
#     ordering = ('email',)


# user/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from medicine_management.models import MedicineReminder  # Import MedicineReminder from the other app
from .models import User

# Inline model to display MedicineReminder in User form
class MedicineReminderInline(admin.TabularInline):
    model = MedicineReminder
    extra = 0  
    fields = ('medicine_name', 'reminder_time', 'recurrence', 'is_taken')
    readonly_fields = ('medicine_name', 'reminder_time', 'recurrence', 'is_taken')  # Optional: To make fields read-only
    verbose_name = 'Medicine Reminder'
    verbose_name_plural = 'Medicine Reminders'

# UserAdmin customization
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'is_active', 'is_staff'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)

    inlines = [MedicineReminderInline]