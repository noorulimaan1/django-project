# from django_celery_beat.models import PeriodicTask, IntervalSchedule
# from celery.schedules import schedule



# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=1,
#     period=IntervalSchedule.MINUTES,
# )

# # Create or update the periodic task
# PeriodicTask.objects.update_or_create(
#     defaults={
#         'interval': schedule,
#         'task': 'ingest_lead_data',  
#     }
# )

# # Create an interval schedule
# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=4,
#     period=IntervalSchedule.HOURS,
# )

# # Create a periodic task
# PeriodicTask.objects.create(
#     interval=schedule,
#     name='Ingest leads every 4 hours',
#     task='api.tasks.ingest_leads',
# )


#celery -A crm worker --loglevel=info
#celery -A crm beat --loglevel=info



