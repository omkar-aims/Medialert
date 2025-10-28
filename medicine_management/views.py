from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MedicineReminderForm ,EditMedicineReminderForm
from .models import MedicineReminder
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json ,pytz
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound,HttpResponse
from medicine_management.tasks import send_refill_reminder ,send_medicine_reminder 

@login_required
def medicine_reminder_view(request):
    if request.method == 'POST':
        form = MedicineReminderForm(request.POST)
        if form.is_valid():
            medicine_name = form.cleaned_data['medicine_name']
            reminder_time = form.cleaned_data['reminder_time']
            notification_method = form.cleaned_data['notification_method']
            recurrence = form.cleaned_data['recurrence']

            exists = MedicineReminder.objects.filter(
                user=request.user,
                medicine_name=medicine_name,
                reminder_time=reminder_time,
                notification_method=notification_method,
                recurrence=recurrence
            ).exists()

            if exists:
                messages.error(request, "You have already added this medicine reminder.")
                return render(request, 'reminders/medicine_reminder.html', {'form': form})

            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()

            if notification_method == 'email':
                hour = reminder_time.hour
                minute = reminder_time.minute

                medicine_reminder_url = request.build_absolute_uri(reverse('medicine_reminder_page'))

                if recurrence == 'every_day':
                    schedule, _ = CrontabSchedule.objects.get_or_create(hour=hour, minute=minute)
                elif recurrence.startswith('every_'):
                    dow_map = {
                        'every_monday':'1', 'every_tuesday':'2', 'every_wednesday':'3',
                        'every_thursday':'4', 'every_friday':'5', 'every_saturday':'6', 'every_sunday':'0'
                    }
                    schedule, _ = CrontabSchedule.objects.get_or_create(hour=hour, minute=minute, day_of_week=dow_map[recurrence])
                elif recurrence == 'today':
                    schedule, _ = CrontabSchedule.objects.get_or_create(hour=hour, minute=minute, day_of_month=str(datetime.now().day))

                PeriodicTask.objects.create(
                    crontab=schedule,
                    name=f"reminder-{reminder.id}-{datetime.now().timestamp()}",
                    task='medicine_management.tasks.send_medicine_email',
                    args=json.dumps([reminder.id])
                )

                messages.success(request, "Medicine reminder added and email scheduled successfully!")
            else:
                messages.success(request, "Medicine reminder added successfully!")

            return redirect('medicine_reminders')
    else:
        form = MedicineReminderForm()

    return render(request, 'reminders/medicine_reminder.html', {'form': form})

def mark_taken_page(request, reminder_id):
    reminder = get_object_or_404(MedicineReminder, id=reminder_id)

    if request.method == "POST":
        reminder.is_taken = True
        reminder.save()
        messages.success(request, f"You've successfully marked {reminder.medicine_name} as taken!")

    return render(request, 'reminders/mark_taken_page.html', {'reminder': reminder})

@login_required
def mark_medicine_taken(request, reminder_id):
    reminder = MedicineReminder.objects.filter(id=reminder_id, user=request.user).first()
    if reminder and reminder.user == request.user:
        reminder.is_taken = True

        if reminder.current_units is not None and reminder.current_units > 0:
            reminder.current_units -= 1

        # Save the updated fields
        reminder.save(update_fields=["is_taken", "current_units"])
        messages.success(request, f"{reminder.medicine_name} marked as taken!")

        # <-- Add refill check here -->
        if reminder.refill_choice == 'yes' and reminder.current_units <= reminder.reminder_threshold:
            from datetime import timedelta
            from django.utils import timezone
            from .tasks import send_refill_reminder

            next_refill_check_time = timezone.now() + timedelta(seconds=5)
            send_refill_reminder.apply_async(
                args=[reminder.id],
                eta=next_refill_check_time
            )
            print("✅ Refill reminder scheduled!")

    else:
        messages.error(request, "Invalid reminder or permission denied.")

    return redirect('medicine_reminders')



@login_required
def medicine_reminder_page(request):
    reminders = MedicineReminder.objects.filter(user=request.user, is_taken=False)
    
    return render(request, 'reminders/medicine_reminder_page.html', {'reminders': reminders})

@login_required
def medicine_reminders_list(request):
    reminders = MedicineReminder.objects.filter(user=request.user)
    return render(request, 'reminders/medicine_reminders_list.html', {'reminders': reminders})

@login_required
def edit_medicine_reminder(request, reminder_id):
    try:
        reminder = MedicineReminder.objects.get(id=reminder_id, user=request.user)
    except MedicineReminder.DoesNotExist:
        return HttpResponseNotFound("Reminder not found.") 

    if request.method == 'POST':
        form = EditMedicineReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('medicine_reminders')
    else:
        form = MedicineReminderForm(instance=reminder)

    return render(request, 'reminders/edit_medicine_reminder.html', {
        'form': form,
        'reminder': reminder,
    })

@login_required
def delete_medicine_reminder(request, reminder_id):
    reminder = get_object_or_404(MedicineReminder, id=reminder_id, user=request.user)
    reminder.delete()
    return redirect('medicine_reminders')
# ------------------------------------------------------------------------------------------------------------
@login_required
def add_medicine_view(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        request.session['medicine_data'] = request.session.get('medicine_data', {})
        request.session['medicine_data']['medicine_name'] = medicine_name
        request.session.modified = True
        print("Medicine name submitted:", medicine_name)
        return redirect(f'/medicine/recurrence_view/')
    else:
        medicine_name = request.session.get('medicine_data', {}).get('medicine_name', '')
    return render(request, 'reminders/add_medicine.html', {'medicine_name': medicine_name})

@login_required
def recurrence_view(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        recurrence = request.POST.get('recurrence')

        request.session['medicine_data'] = request.session.get('medicine_data', {})
        request.session['medicine_data']['medicine_name'] = medicine_name
        request.session['medicine_data']['recurrence'] = recurrence
        request.session.modified = True

        print("Medicine:", medicine_name)
        print("Recurrence:", recurrence)

        return redirect('reminder_details')
    else:
        medicine_name = request.GET.get('medicine_name', '') or request.session.get('medicine_data', {}).get('medicine_name', '')
        recurrence = request.session.get('medicine_data', {}).get('recurrence', '')
    return render(request, 'reminders/recurrence_view.html', {'medicine_name': medicine_name, 'recurrence': recurrence})

@login_required
def summary_page(request):
    medicine_data = request.session.get('medicine_data', {})
    return render(request, 'reminders/summary.html', {'medicine_data': medicine_data})

@login_required
def reminder_details_view(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name') or request.session.get('medicine_data', {}).get('medicine_name')
        recurrence = request.POST.get('recurrence') or request.session.get('medicine_data', {}).get('recurrence')
        reminder_time_str = request.POST.get('reminder_time')
        dose = request.POST.get('dose')
        notification_method = request.POST.get('notification_method')  # email or sms
        notification_email = request.POST.get('notification_email') if notification_method == 'email' else None
        notification_phone = request.POST.get('notification_phone') if notification_method == 'sms' else None


        request.session['medicine_data'] = {
            'medicine_name': medicine_name,
            'recurrence': recurrence,
            'reminder_time': reminder_time_str,
            'dose': dose
        }

        reminder = MedicineReminder.objects.create(
            user=request.user,
            medicine_name=medicine_name,
            dose=dose,
            reminder_time=reminder_time_str,
            recurrence=recurrence if recurrence else 'every_day',
            notification_method=notification_method,
            notification_email=notification_email,
            notification_phone=notification_phone,
            status='processing'
        )

        local_tz = pytz.timezone('Asia/Kolkata')
        reminder_time = datetime.strptime(reminder_time_str, "%H:%M").time()
        reminder_datetime = datetime.combine(datetime.today(), reminder_time)
        reminder_datetime = local_tz.localize(reminder_datetime)

        if reminder_datetime < timezone.now():
            reminder_datetime += timedelta(days=1)

        send_medicine_reminder.apply_async(args=[reminder.id], eta=reminder_datetime)
        
        
        return redirect('refill_reminder')

    medicine_name = request.session.get('medicine_data', {}).get('medicine_name', '')
    recurrence = request.session.get('medicine_data', {}).get('recurrence', '')
    reminder_time = request.session.get('medicine_data', {}).get('reminder_time', '')
    dose = request.session.get('medicine_data', {}).get('dose', '')

    return render(request, 'reminders/reminder_details.html', {
        'medicine_name': medicine_name,
        'recurrence': recurrence,
        'reminder_time': reminder_time,
        'dose': dose
    })


@login_required
def refill_reminder_view(request):
    medicine_name = request.POST.get('medicine_name') or request.session.get('medicine_data', {}).get('medicine_name')
    recurrence = request.POST.get('recurrence') or request.session.get('medicine_data', {}).get('recurrence')
    reminder_time_str = request.POST.get('reminder_time') or request.session.get('medicine_data', {}).get('reminder_time')
    dose = request.POST.get('dose') or request.session.get('medicine_data', {}).get('dose')

    if not medicine_name:
        messages.error(request, "Medicine name is required to set a refill reminder.")
        return redirect('dashboard')

    if request.method == 'POST':
        refill_choice = request.POST.get('refill')

        reminder = MedicineReminder.objects.filter(
            user=request.user,
            medicine_name=medicine_name
        ).first()

        if reminder:
            reminder.refill_choice = 'no'
            reminder.save()
            messages.info(request, "Reminder updated with 'No' refill choice.")
        else:
            MedicineReminder.objects.create(
                user=request.user,
                medicine_name=medicine_name,
                recurrence=recurrence,
                reminder_time=reminder_time_str,
                dose=dose,
                refill_choice='no',  
                status='processing'
            )

        return redirect('dashboard')

    return render(request, 'reminders/refill_reminder.html', {
        'medicine_name': medicine_name,
        'recurrence': recurrence,
        'reminder_time': reminder_time_str,
        'dose': dose
    })



@login_required
def no_reason_page(request):
    """
    Display the form where the user can enter a reason for not refilling.
    """
    return render(request, 'reminders/no_reason.html')

@login_required
def submit_no_reason(request):
    if request.method == 'POST':
        reason = request.POST.get('reason')
        print("User reason for not refilling:", reason)
        messages.success(request, "Thank you for your feedback!")
        return redirect('dashboard')  
    return redirect('dashboard')

@login_required
def yes_refill_page(request):
    return render(request, 'reminders/yes_refill.html')


@login_required
def submit_yes_reason(request):
    if request.method == 'POST':
        current_units = int(request.POST.get('current_units'))
        reminder_threshold = int(request.POST.get('reminder_threshold'))
        email_reminder = request.POST.get('email_reminder') 
        medicine_name = request.session.get('medicine_data', {}).get('medicine_name')
        reminder_time_str = request.session.get('medicine_data', {}).get('reminder_time')

        if not medicine_name or not reminder_time_str:
            messages.error(request, "Medicine name and reminder time are required.")
            return redirect('dashboard')

        reminder_time = datetime.strptime(reminder_time_str, "%H:%M").time()
        local_tz = pytz.timezone('Asia/Kolkata')
        reminder_datetime = datetime.combine(datetime.today(), reminder_time)
        reminder_datetime = local_tz.localize(reminder_datetime)

        if reminder_datetime < timezone.now():
            reminder_datetime += timedelta(days=1)

        reminder = MedicineReminder.objects.filter(user=request.user, medicine_name=medicine_name).first()

        if reminder:
            reminder.refill_choice = 'yes'
            reminder.current_units = current_units
            reminder.reminder_threshold = reminder_threshold
            reminder.notification_email = email_reminder
            reminder.reminder_time = reminder_time  
            reminder.status = 'processing'
            reminder.save()

        if reminder.refill_choice == 'yes' and reminder.current_units <= reminder.reminder_threshold:

            messages.success(request, "Refill reminder successfully updated!")
        else:
            reminder = MedicineReminder.objects.create(
                user=request.user,
                medicine_name=medicine_name,
                refill_choice='yes',
                current_units=current_units,
                reminder_threshold=reminder_threshold,
                notification_email=email_reminder,
                reminder_time=reminder_time,
                status='processing'
            )
            messages.success(request, "Refill reminder successfully created!")

        if current_units <= reminder_threshold:
            next_refill_check_time = reminder_datetime + timedelta(seconds=10)  
            send_refill_reminder.apply_async(
                args=[reminder.id],  
                eta=next_refill_check_time
            )

        return redirect('no_reason_page')