from django.contrib import admin
from .models import MedicineReminder

@admin.register(MedicineReminder)
class MedicineReminderAdmin(admin.ModelAdmin):
    list_display = (
        'medicine_name', 'dose', 'reminder_time', 'refill_choice', 'notification_method',
        'recurrence', 'status', 'last_sent_time', 'user', 'is_taken', 'notification_email',
        'notification_phone', 'current_units', 'reminder_threshold', 'reminder_date'
    )
    
    search_fields = ('medicine_name', 'notification_email', 'notification_phone')
    list_filter = ('notification_method', 'recurrence', 'status', 'is_taken')
    ordering = ('reminder_time',)
    
    def is_taken(self, obj):
        """
        Returns the number of units taken by the user.
        """
        return obj.is_taken
    is_taken.admin_order_field = 'is_taken'
    is_taken.short_description = 'Medicines Taken'
    
    def remaining_units(self, obj):
        """
        Returns the remaining units after subtracting taken units.
        """
        return obj.current_units - obj.is_taken
    remaining_units.admin_order_field = 'remaining_units'
    remaining_units.short_description = 'Remaining Units'
