from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from medicine_management.tasks import send_medicine_email

def schedule_medicine_email(reminder):
    reminder_time = reminder.reminder_time  # This is a time object
    current_time = now()  # Aware datetime

    # Combine today's date with the reminder time to make a naive datetime
    scheduled_datetime = datetime.combine(current_time.date(), reminder_time)

    # Make scheduled_datetime aware in the same timezone as current_time
    scheduled_datetime = make_aware(scheduled_datetime)

    # If it's already past for today, schedule for tomorrow
    if scheduled_datetime < current_time:
        scheduled_datetime += timedelta(days=1)

    delay_seconds = (scheduled_datetime - current_time).total_seconds()

    send_medicine_email.apply_async(args=[reminder.id], countdown=delay_seconds)
