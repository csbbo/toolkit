from typing import List, Union

from django.db.models import Q

from common.utils import tushare_utils
from stock.models import Quote, Stock


def batch_save_stocks(items: list, batch_size: int = 100) -> None:
    update_fields: List[str] = []
    unique_fields = ["ts_code"]

    bulk_create_list = []
    for item in items:
        if not update_fields:
            update_fields = [x for x in item.keys() if x not in unique_fields]
        bulk_create_list.append(Stock(**item))

    Stock.objects.bulk_create(
        bulk_create_list,
        batch_size=batch_size,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=unique_fields,
    )


def batch_save_quotes(items: list, batch_size: int = 100) -> None:
    update_fields: List[str] = []
    unique_fields = ["stock_id", "date"]

    bulk_create_list = []
    for item in items:
        if not update_fields:
            update_fields = [x for x in item.keys() if x not in unique_fields]
        bulk_create_list.append(Quote(**item))

    Quote.objects.bulk_create(
        bulk_create_list,
        batch_size=batch_size,
        update_conflicts=True,
        update_fields=update_fields,
        unique_fields=unique_fields,
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
