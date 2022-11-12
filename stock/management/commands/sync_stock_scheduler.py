import logging
from typing import Any

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand
from django.utils import timezone

from common.utils import date_utils
from common.utils.tushare_utils import fetch_stocks, get_quotes
from stock.models import Stock
from stock.utils import batch_save_quotes, batch_save_stocks

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def sync_stocks() -> None:
    logger.info("sync_stocks: start")

    items = []
    batch_size = 1000

    for data in fetch_stocks():
        items.append(data)

        if len(items) >= batch_size:
            batch_save_stocks(items=items, batch_size=batch_size)
            items = []
    if items:
        batch_save_stocks(items=items, batch_size=batch_size)

    logger.info("sync_stocks: finish")


def sync_stock_quotes() -> None:
    logger.info("sync_stock_quotes: start")

    ts_code_map: dict = {}
    batch_size = 100

    def handle_results(result_list: list) -> None:
        for result in result_list:
            result.pop("name", "")
            ts_code = result.pop("ts_code", "")
            trade_time = result.pop("datetime", "")

            trade_time = date_utils.str2datetime(trade_time, fmt="%Y%m%d%H%M%S")
            result["date"] = trade_time
            result["stock_id"] = ts_code_map.get(ts_code)

    for stock in Stock.objects.values("id", "ts_code").all():
        ts_code_map[stock["ts_code"]] = stock["id"]

        if len(ts_code_map) > batch_size:
            results = get_quotes(ts_codes=list(ts_code_map.keys()))
            handle_results(results)

            batch_save_quotes(items=results, batch_size=batch_size)
            ts_code_map = {}

    if ts_code_map:
        results = get_quotes(ts_codes=list(ts_code_map.keys()))
        handle_results(results)

        batch_save_quotes(items=results, batch_size=batch_size)

    logger.info("sync_stock_quotes: finish")


class Command(BaseCommand):
    help = "Sync Stocks"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--run_now", type=str, default="true")

    def handle(self, *args: list, **options: dict) -> None:
        run_now = options["run_now"]

        # https://apscheduler.readthedocs.io/en/3.x/userguide.html
        scheduler = BlockingScheduler()

        scheduler.add_job(
            sync_stocks,
            "interval",
            days=0,
            hours=8,
            minutes=0,
            seconds=0,
            next_run_time=timezone.now() if str(run_now) == "true" else None,
        )

        # https://tool.lu/crontab/
        scheduler.add_job(
            sync_stock_quotes,
            "cron",
            minute="*/5",
            hour="9-16",
            day="*",
            month="*",
            day_of_week="1-5",
            next_run_time=timezone.now() if str(run_now) == "true" else None,
        )

        self.stdout.write(self.style.SUCCESS("running sync stocks scheduler task..."))

        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            self.stdout.write(self.style.SUCCESS("terminal sync stocks scheduler task"))
