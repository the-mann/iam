from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every minute
    RETRY_AFTER_FAILURE_MINS = 1
    ALLOW_PARALLEL_RUNS = True

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'main.my_cron_job'  # a unique code

    def do(self):
        print("why hello there")
