from common.constants import Constant


class LogType(Constant):
    STOCK_OP = 1

    CHOICES = ((STOCK_OP, "Stock"),)


class ScheduleTrigger(Constant):
    DATE = "date"
    INTERVAL = "interval"
    CRON = "cron"

    CHOICES = (
        (DATE, "date"),
        (INTERVAL, "interval"),
        (CRON, "cron"),
    )
