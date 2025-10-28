from django.urls import path
from . import views

urlpatterns = [
    path('reminder/', views.medicine_reminder_view, name='medicine_reminder'),
    path('reminders/', views.medicine_reminders_list, name='medicine_reminders'),
    path('mark_taken/<int:reminder_id>/', views.mark_medicine_taken, name='mark_medicine_taken'),
    path('mark_taken_page/<int:reminder_id>/', views.mark_taken_page, name='mark_taken_page'),
    path('medicine_reminder_page/', views.medicine_reminder_page, name='medicine_reminder_page'), 
    path('reminders/edit/<int:reminder_id>/', views.edit_medicine_reminder, name='edit_medicine_reminder'),
    path('reminders/delete/<int:reminder_id>/', views.delete_medicine_reminder, name='delete_medicine_reminder'),
    path('', views.add_medicine_view, name='add_medicine'),
    path('recurrence_view/', views.recurrence_view, name='recurrence_view'),  
    path('reminder_details', views.reminder_details_view, name='reminder_details'),
    path('refill_reminder/', views.refill_reminder_view, name='refill_reminder'),
    path('no-reason/', views.no_reason_page, name='no_reason_page'),
    path('submit-no-reason/', views.submit_no_reason, name='submit_no_reason'),
    path('yes-refill/', views.yes_refill_page, name='yes_refill'),  
    path('submit-yes-reason/', views.submit_yes_reason, name='submit_yes_reason'),
    path('summary/' ,views.summary_page , name = 'summary'),

] 