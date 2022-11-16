import logging
import time
from typing import Any

import dramatiq
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand

from common.models import ScheduleTask

logger = logging.getLogger(__name__)

broker = dramatiq.get_broker()


def send_task(*args: list, **kwargs: dict) -> None:
    task_name = kwargs.pop("_task_name")
    func = broker.get_actor(task_name)

    message = func.send_with_options(*args, **kwargs)
    msg_id = message.message_id
    # see: https://github.com/Bogdanp/django_dramatiq/issues/44#issuecomment-511375731
    broker.connection.close()

    sleep_secs = 3
    while True:
        try:
            message.get_result(block=False)
            logger.info(f"Task: {func}, finished successfully, message: {msg_id}")
            break
        except Exception:
            logger.info(
                f"Task: {func}, wait for message: {msg_id} finished, sleep for {sleep_secs} secs"
            )
            time.sleep(sleep_secs)
            pass


class Command(BaseCommand):
    help = "Sync Stocks"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--run_now", type=str, default="true")

    def handle(self, *args: list, **options: dict) -> None:
        # run_now = options["run_now"]

        # https://apscheduler.readthedocs.io/en/3.x/userguide.html
        scheduler = BlockingScheduler()

        for task in ScheduleTask.objects.all():
            scheduler.add_job(
                func=send_task,
                args=task.args,
                kwargs={"_task_name": task.actor_name, **task.kwargs},
                trigger=task.trigger,
                **task.config,
            )

        self.stdout.write(self.style.SUCCESS("running sync stocks scheduler task..."))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("terminal sync stocks scheduler task"))
