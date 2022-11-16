import logging
import time
from typing import Any

import dramatiq
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand

from common.models import ScheduleTask

logger = logging.getLogger(__name__)

broker = dramatiq.get_broker()


def send_task(**kwargs: dict) -> None:
    print(kwargs)
    task_name = kwargs.get("task_name", "")
    func = broker.get_actor(task_name)
    task_kwargs = kwargs.get("task_kwargs", {})
    task_priority = kwargs.get("task_priority", 100)

    message = func.send_with_options(kwargs=task_kwargs, priority=task_priority)
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
            time.sleep(3)
            pass


class Command(BaseCommand):
    help = "Scheduler task"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--run_now", type=str, default="true")

    def handle(self, *args: list, **options: dict) -> None:
        # run_now = options["run_now"]

        # https://apscheduler.readthedocs.io/en/3.x/userguide.html
        scheduler = BlockingScheduler()

        for task in ScheduleTask.objects.filter(enabled=True):
            job_kwargs = {
                "task_name": task.actor_name,
                "task_kwargs": task.kwargs,  # 任务只支持传kwargs, 不支持传args
                "task_priority": task.priority,
            }
            scheduler.add_job(
                func=send_task,
                kwargs=job_kwargs,
                trigger=task.trigger,
                **task.config,
            )

        self.stdout.write(self.style.SUCCESS("running sync stocks scheduler task..."))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("terminal sync stocks scheduler task"))
