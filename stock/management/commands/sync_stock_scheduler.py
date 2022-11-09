import datetime
import logging
from typing import Any

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand
from django.utils import timezone

from common.utils.tushare_utils import fetch_stocks
from stock.utils import batch_save_stocks

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def sync_task() -> None:
    items = []
    batch_size = 1000
    for data in fetch_stocks():
        items.append(data)

        if len(items) > batch_size:
            batch_save_stocks(items=items, batch_size=batch_size)
            items = []
            logger.info("sync...")
    if items:
        batch_save_stocks(items=items, batch_size=batch_size)

    now = datetime.datetime.now()
    logger.info(f"sync stock finish: {now}")


class Command(BaseCommand):
    help = "Sync Stocks"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--days", type=int, default=0)
        parser.add_argument("--hours", type=int, default=8)
        parser.add_argument("--minutes", type=int, default=0)
        parser.add_argument("--seconds", type=int, default=0)
        parser.add_argument("--run_now", type=str, default="true")

    def handle(self, *args: list, **options: dict) -> None:
        days = options["days"]
        hours = options["hours"]
        minutes = options["minutes"]
        seconds = options["seconds"]
        run_now = options["run_now"]

        # https://apscheduler.readthedocs.io/en/3.x/userguide.html
        scheduler = BlockingScheduler()
        scheduler.add_job(
            sync_task,
            "interval",
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            next_run_time=timezone.now() if str(run_now) == "true" else None,
        )
        self.stdout.write(self.style.SUCCESS("running sync stocks scheduler task..."))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("terminal sync stocks scheduler task"))
