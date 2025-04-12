from django_cron import CronJobBase, Schedule
from bookings.management.commands.send_reminders import Command

class SendReminderEmailsCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # once every hour (change as needed)

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bookings.send_reminders_cron'  # unique identifier

    def do(self):
        print("Running SendReminderEmailsCronJob...")
        Command().handle()
