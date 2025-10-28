from django.utils.timezone import make_aware, now
from medicine_management.tasks import send_medicine_email

def schedule_medicine_email(reminder):
    reminder_time = reminder.reminder_time

    # Make aware if naive
    if reminder_time.tzinfo is None:
        reminder_time = make_aware(reminder_time)

    current_time = now()
    delay_seconds = (reminder_time - current_time).total_seconds()
    if delay_seconds < 0:
        delay_seconds = 0  # send immediately if time passed

    send_medicine_email.apply_async(args=[reminder.id], countdown=delay_seconds)
