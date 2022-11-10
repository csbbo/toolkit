from typing import Union

from django.db.models import Q

from common.utils import tushare_utils
from common.utils.str_utils import chinese2pinyin_initials
from stock.models import Stock


def batch_save_stocks(items: list, batch_size: int = 100) -> None:
    bulk_create_list = []
    for item in items:
        item["pinyin"] = chinese2pinyin_initials(item["name"])
        bulk_create_list.append(Stock(**item))
    Stock.objects.bulk_create(
        bulk_create_list, ignore_conflicts=True, batch_size=batch_size
    )


def get_stock_market_info(search: Union[str, list]) -> str:
    """
    实时行情信息
    """
    results = []
    if isinstance(search, str):
        search = [search]

    for s in search:
        queryset = Stock.objects.filter(
            Q(ts_code=s) | Q(symbol=s) | Q(pinyin__icontains=s) | Q(name__icontains=s)
        )[:20]

        for stock in queryset:
            name = stock.name
            ts_code = stock.ts_code
            price, rose = tushare_utils.get_real_time_market(ts_code)
            if not (price and rose):
                results.append(price)
                continue

            results.append(f"{name} {price} {rose}%")
    return "\n".join(results) + "\n"
