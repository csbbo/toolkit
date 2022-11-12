import zoneinfo
from datetime import date, datetime

DEFAULT_TIMEZONE = "Asia/Shanghai"


def str2datetime(
    value: str, fmt: str = "%Y-%m-%d %H:%M:%S", tz: str = DEFAULT_TIMEZONE
) -> datetime:
    tzinfo = zoneinfo.ZoneInfo(tz)
    return datetime.strptime(value, fmt).replace(tzinfo=tzinfo)


def format_datetime(obj: date, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return obj.strftime(fmt)
