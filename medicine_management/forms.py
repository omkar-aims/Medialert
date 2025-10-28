from django import forms
from .models import MedicineReminder

class MedicineReminderForm(forms.ModelForm):
    class Meta:
        model = MedicineReminder
        fields = ['medicine_name', 'recurrence', 'reminder_time', 'notification_method','notification_email']

    notification_method = forms.ChoiceField(
        choices=[('email', 'Email'), ('sms', 'SMS')]
    )

class EditMedicineReminderForm(forms.ModelForm):
    class Meta:
        model = MedicineReminder
        fields = ['medicine_name', 'reminder_time', 'notification_method', 'recurrence','notification_email']
        widgets = {
            'reminder_time': forms.TimeInput(attrs={'type': 'time'}),
        }