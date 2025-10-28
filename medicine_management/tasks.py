from celery import shared_task
from .models import MedicineReminder
from .utils.mailgun_helper import send_medicine_email

@shared_task
def send_medicine_reminder(reminder_id):
    reminder = MedicineReminder.objects.get(id=reminder_id)
    link = f"http://127.0.0.1:8000/medicine/mark_taken_page/{reminder.id}/"
    subject = f"Medicine Reminder: {reminder.medicine_name}"

    html_message = f"""
    <html>
        <body style="margin:0; padding:0; background-color:#f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f4f4; padding: 20px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; border-radius: 8px; overflow: hidden; font-family: Arial, sans-serif; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                            <tr>
                                <td align="center" style="background-color:#4CAF50; padding: 20px;">
                                    <h1 style="color:#ffffff; margin:0;">MediAlert</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 30px;">
                                    <h2 style="color:#333333;">Time to Take Your Medicine!</h2>
                                    <p style="color:#555555; font-size: 16px; line-height: 1.5;">
                                        Hello! 👋<br><br>
                                        This is a friendly reminder to take your medicine:
                                    </p>
                                    <table style="margin: 20px 0; border-collapse: collapse; width: 100%;">
                                        <tr>
                                            <td style="padding: 10px; background-color:#f0f0f0; border-radius: 4px;">
                                                <strong>Medicine Name:</strong> {reminder.medicine_name}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 10px; background-color:#f0f0f0; border-radius: 4px; margin-top: 10px;">
                                                <strong>Dose:</strong> {reminder.dose}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 10px; background-color:#f0f0f0; border-radius: 4px; margin-top: 10px;">
                                                <strong>Time:</strong> {reminder.reminder_time}
                                            </td>
                                        </tr>
                                    </table>
                                    <p style="color:#555555; font-size:14px; margin-top:20px;">
                                        After taking your medicine, please visit this link to mark it as taken:
                                        <span style="color:#555555; text-decoration: none;">
                                            http://127.0.0.1:8000/medicine/mark_taken_page/{reminder.id}/
                                        </span>
                                    </p>
                                    <p style="color:#888888; font-size: 14px;">Stay well,<br>MediAlert Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="background-color:#f9f9f9; padding: 15px; font-size: 12px; color: #aaa;">
                                    This is an automated reminder. Do not reply to this email.
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """

    send_medicine_email(
        subject,
        message=None,
        html_message=html_message,
        recipient_email=reminder.notification_email
    )

@shared_task
def send_refill_reminder(reminder_id):
    reminder = MedicineReminder.objects.get(id=reminder_id)
    link = f"http://127.0.0.1:8000/medicine/mark_taken_page/{reminder.id}/"
    subject = f"Refill Reminder: {reminder.medicine_name}"

    html_message = f"""
    <html>
        <body style="margin:0; padding:0; background-color:#f4f4f4;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f4f4; padding: 20px 0;">
                <tr>
                    <td align="center">
                        <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff; border-radius: 8px; overflow: hidden; font-family: Arial, sans-serif; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                            <tr>
                                <td align="center" style="background-color:#FF9800; padding: 20px;">
                                    <h1 style="color:#ffffff; margin:0;">MediAlert</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 30px;">
                                    <h2 style="color:#333333;">Time to Refill Your Medicine!</h2>
                                    <p style="color:#555555; font-size: 16px; line-height: 1.5;">
                                        Hello! 👋<br><br>
                                        Your medicine is running low:
                                    </p>
                                    <table style="margin: 20px 0; border-collapse: collapse; width: 100%;">
                                        <tr>
                                            <td style="padding: 10px; background-color:#f0f0f0; border-radius: 4px;">
                                                <strong>Medicine Name:</strong> {reminder.medicine_name}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 10px; background-color:#f0f0f0; border-radius: 4px;">
                                                <strong>Current Units:</strong> {reminder.current_units}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 10px; background-color:#f0f0f0; border-radius: 4px;">
                                                <strong>Reminder Threshold:</strong> {reminder.reminder_threshold}
                                            </td>
                                        </tr>
                                    </table>
                                
                                    <p style="color:#888888; font-size: 14px;">Stay well,<br>MediAlert Team</p>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="background-color:#f9f9f9; padding: 15px; font-size: 12px; color: #aaa;">
                                    This is an automated reminder. Do not reply to this email.
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """

    send_medicine_email(
        subject,
        message=None,
        html_message=html_message,
        recipient_email=reminder.notification_email
    )

