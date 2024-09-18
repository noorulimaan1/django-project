from django_celery_beat.models import PeriodicTask, IntervalSchedule

from celery.schedules import schedule


# The interval schedule
schedule, created = IntervalSchedule.objects.get_or_create(
    every=4,
    period=IntervalSchedule.HOURS,
)

# The periodic task
PeriodicTask.objects.create(
    interval=schedule,
    name='Ingest leads every 4 hours',
    task='api.tasks.ingest_leads',
)
