from django.db import models
from django.conf import settings
from datetime import date

class MedicineReminder(models.Model):
    RECURRING_CHOICES = [
    ('once_a_day', 'Once a day'),
    ('twice_a_day', 'Twice a day'),
    ('thrice_a_day', 'Thrice a day'),
    ('today', 'Today'),
    ('every_day', 'Every day'),
    ('every_monday', 'Every Monday'),
    ('every_tuesday', 'Every Tuesday'),
    ('every_wednesday', 'Every Wednesday'),
    ('every_thursday', 'Every Thursday'),
    ('every_friday', 'Every Friday'),
    ('every_saturday', 'Every Saturday'),
    ('every_sunday', 'Every Sunday'),]


    NOTIFICATION_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]

    REFILL_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),]

    medicine_name = models.CharField(max_length=100)
    reminder_time = models.TimeField(null=True, blank=True)
    notification_method = models.CharField(
        max_length=10,
        choices=NOTIFICATION_CHOICES
    )
    recurrence = models.CharField(
        max_length=50,
        choices=RECURRING_CHOICES,
        default='every_day'  
    )
    status = models.CharField(max_length=10, choices=[('processing', 'Processing'), ('sent', 'Sent'), ('failed', 'Failed')], default='processing')
    last_sent_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    is_taken = models.BooleanField(default=False)
    notification_email = models.EmailField(null=True, blank=True)
    notification_phone = models.CharField(max_length=15, null=True, blank=True)
    dose = models.CharField(max_length=50, null=True, blank=True)  
    refill_choice = models.CharField(
    max_length=3,
    choices=REFILL_CHOICES)
    current_units = models.PositiveIntegerField(null=True, blank=True)
    reminder_threshold = models.PositiveIntegerField(null=True, blank=True)
    reminder_date = models.DateField(null=True, blank=True)

   
    def __str__(self):
        return f'{self.medicine_name} Reminder - {self.recurrence} at {self.reminder_time} (Dose: {self.dose})'
    
    def reset_status_if_needed(self):
        if self.last_sent_time is None or self.last_sent_time.date() < date.today():
            self.status = 'processing'
            self.save()
    
    def check_reminder(self):
        """
        This method checks if the reminder should be sent.
        If the number of units remaining is less than or equal to the reminder threshold,
        it will trigger the reminder.
        """
        remaining_units = self.current_units - self.is_taken
        if remaining_units <= self.reminder_threshold:
            self.trigger_reminder()

    def trigger_reminder(self):
        """
        Temporary logic to trigger a reminder when the threshold is met.
        Right now, this just prints a message. Later, we can send an email.
        """
        print(f"Reminder: You have {self.reminder_threshold} medicines left. Time to refill!")